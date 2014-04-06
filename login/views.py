from django.views.generic import View
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from armadillo_reuse.settings import SERVER_PORT, MAIN_URL
import hashlib
import jsonpickle

class SignupView(View):
    """This class handles all requests from client that
    have to do with Login/Signup/Deactivate ...
    It creates the server entry for a client and establishes
    the security protocol/token on both server and client.

    Expects a post request from client as per the api
    specifications.
    """

    def post(self, request, *args, **kwargs):

        client_email = request.POST['email']

        if self.validate_mit_email(client_email):

            #generate hashed token seed by email address.
            token = hashlib.sha224(client_email+"@armadillo.reuse").hexdigest()

            #TODO: include device id during initialization to set up GCM push notifications gcm_id?
            client_user = User.objects.create_user(username=client_email, email=client_email, password=token)
            client_user.is_active = False
            client_user.save()

            verify_subject = "Your REUSE Mobile account verification"

            verify_message = "Please verify your account here: http://%s:%s/api/login/verify/?username=%s&token=%s" % (MAIN_URL, SERVER_PORT, client_email, token)
            verify_from = "no-reply@armadillo.xvm.mit.edu"
            verify_to = [client_email]

            #TODO: Fail loud?
            send_mail(verify_subject, verify_message, verify_from, verify_to, fail_silently=False)

            response = jsonpickle.encode({"success" : True})
            return HttpResponse(response, content_type="application/json")
        else:
            return HttpResponseForbidden("Invalid Request.")


    def validate_mit_email(self, email):
        """validates that email is not only a valid
        email address but also an MIT email address

        returns true/false
        """

        return True

class VerifyView(View):
    """ This class receives verification requests sent
    when client clicks on verification link sent through
    their email from api-server

    Expects GET request
    """

    def get(self, request, *args, **kwargs):

        client_token = request.GET['token']
        client_username = request.GET['username']
        client_user = authenticate(username=client_username, password=client_token)

        if client_user is not None and not client_user.is_active:
            client_user.is_active = True
            client_user.save()

            #TODO: push token to client device. client.gcm_id ?

            response = "Thank you for verifying your account, %s. Enjoy using Reuse Mobile." % client_user.username

            return HttpResponse(response, content_type="text/plain")
        else:
            return HttpResponseForbidden("Invalid Request.")