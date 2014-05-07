from django.views.generic import View
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from web_api.models import GcmUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from armadillo_reuse.settings import SERVER_PORT, MAIN_URL, DEBUG
import hashlib
import jsonpickle
from validate_email import validate_email
from utils.utils import send_gcm_message, send_mail
import logging
from threads.views import AbstractThreadView
logger = logging.getLogger('armadillo')


class SignupView(View):
    """This class handles all requests from client that
    have to do with Login/Signup/Deactivate ...
    It creates the server entry for a client and establishes
    the security protocol/token on both server and client.

    Expects a post request from client as per the api
    specifications.
    """

    def post(self, request, *args, **kwargs):
        try:
            client_email = request.POST['email']
            client_gcm_id = request.POST['gcm_id']

            if self.validate_mit_email(client_email):

                #generate hashed token seed by email address.
                token = hashlib.sha224(client_email+"@armadillo.reuse").hexdigest()

                verify_subject = "Your REUSE Mobile account verification"

                verify_message = "Please verify your account here: http://%s:%s/api/login/verify/?username=%s&token=%s" % (MAIN_URL, SERVER_PORT, client_email, token)
                verify_from = "no-reply@armadillo.xvm.mit.edu"
                verify_to = [client_email]

                #TODO: Fail loud?

                status = send_mail(verify_from, verify_to, verify_subject, verify_message)

                if status == "success":
                    client_user = None
                    try:
                        client_user = User.objects.all().get(username=client_email)
                    except Exception as e:
                        pass
                    if client_user is not None:
                        client_user.is_active = False
                        client_user.save()
                    else:
                        client_user = User.objects.create_user(username=client_email, email=client_email, password=token)
                        client_user.is_active = False
                        client_gcm_user = GcmUser.objects.create(user=client_user, gcm_id=client_gcm_id)
                        client_user.save()

                    response = jsonpickle.encode({"success": True})
                    return HttpResponse(response, content_type="application/json")
                else:
                    logger.error("SIGNUP: " + status + '\n\n')
                    return HttpResponseServerError("Please try again." + "\n\n\n" + status)
            else:
                return HttpResponseForbidden("Invalid Request.")

        except Exception as e:
            logger.exception(str(e))
            return HttpResponseServerError(e if DEBUG else "An error has occured.")

    def validate_mit_email(self, email):
        """validates that email is not only a valid
        email address but also an MIT email address

        returns true/false
        """
        ans = validate_email(email) and (email.endswith(".mit.edu") or email.endswith("@mit.edu"))
        if ans:
            return True
        else:
            logger.info("VALIDATE: User with email address " + email + " denied sign up." + '\n\n')
            return False

class VerifyView(View):
    """ This class receives verification requests sent
    when client clicks on verification link sent through
    their email from api-server

    Expects GET request
    """

    def get(self, request, *args, **kwargs):

        try:
            client_token = request.GET['token']
            client_username = request.GET['username']
            client_user = authenticate(username=client_username, password=client_token)

            if client_user is not None and not client_user.is_active:
                client_user.is_active = True
                client_user.save()

                #Send gcm token
                data = {'token': client_token}
                client_gcm_id = GcmUser.objects.get(user=client_user).gcm_id
                res = send_gcm_message([client_gcm_id], data, 'token')

                response = "Thank you for verifying your account, %s. Enjoy using Reuse Mobile." % client_user.username

                return HttpResponse(response, content_type="text/plain")
            else:
                logger.info("VERIFY: User with USERNAME: " + client_username + " TOKEN: " + client_token + " denied verification." + '\n\n')
                return HttpResponseForbidden("Invalid Request.")

        except Exception as e:
            logger.exception(str(e))
            return HttpResponseServerError(e if DEBUG else "An error has occured.")


class UnregisterView(View):
    """ This class removes the client from the
    Reuse Server

    Expects POST request
    """

    def post(self, request, *args, **kwargs):

        try:
            auth_thread = AbstractThreadView()
            client_user = auth_thread.authenticate_user(request, args, kwargs)

            if client_user is not None and client_user.is_active:
                client_gcm = GcmUser.objects.get(email=client_user.email)
                client_gcm.delete()
                client_user.delete()

                response = jsonpickle.encode({"success": True})
                return HttpResponse(response, content_type="application/json")
            else:
                logger.info("UNREGISTER: User with USERNAME: " + client_user.username + " TOKEN: " + request.HEADERS['token'] + " denied unregistration." + '\n\n')
                return HttpResponseForbidden("Invalid Request.")

        except Exception as e:
            logger.exception(str(e))
            return HttpResponseServerError(e if DEBUG else "An error has occured.")
