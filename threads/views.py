from django.views.generic import View
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from web_api.models import *
import jsonpickle
from django.core import serializers
from utils.utils import send_mail
from armadillo_reuse.settings import REUSE_EMAIL_ADDRESS, MAIN_URL
from django.contrib.auth import authenticate
from web_api.location.ItemPostLocator import ItemPostLocator
import time


class AbstractThreadView(View):
    """ A base class for all Thread handler views.
    """
    def authenticate_user(self, request, *args, **kwargs):
        """Authenticates user and if it is a valid request,
        identifies and returns the client's User object

        Returns None if authentication fails for whatever reason
        """

        if 'HTTP_USERNAME' in request.META and 'HTTP_TOKEN' in request.META:
            username = request.META['HTTP_USERNAME']
            token = request.META['HTTP_TOKEN']
            client_user = authenticate(username=username, password=token)
            if client_user is not None and client_user.is_active:
                return client_user
            else:
                return None

        return None


class ThreadGetView(AbstractThreadView):
    """This view handles client requests to get an
    update of all items that have been modified
    since the specified time as per client's request

    It queries and fetches data from database.

    Expects GET request from client as per the api
    specifications.
    """

    def get(self, request, *args, **kwargs):

        client = self.authenticate_user(request, *args, **kwargs)

        if client is not None:

            if not 'after' in request.GET:
                return HttpResponseBadRequest("Cannot find 'after' attribute")

            after = request.GET['after']
            update_items = Item.objects.all().filter(modified__gte=after)

            response_items = serializers.serialize('json', update_items)

            return HttpResponse(response_items)
        else:
            return HttpResponseForbidden("Invalid Request.")


class ThreadPostView(AbstractThreadView):
    """This view handles posting an new item
    into the system. It retrieves data from the request
    and creates a new thread and inserts an item into
    the appropriate place in database.
    It also sends an email to the reuse list for the post.

    Expects a POST request from client as per the api
    specifications
    """

    def post(self, request, *args, **kwargs):

        client = self.authenticate_user(request, *args, **kwargs)

        if client is not None:

            attributes = ['name', 'description', 'location', 'tags']
            for attribute in attributes:
                if not attribute in request.POST:
                    return HttpResponseBadRequest("Cannot find '%s' attribute" % attribute)

            subject = request.POST['name']
            sender = client.email
            shameless_plug = "SENT USING REUSE MOBILE APP. GET IT AT armadillo.xvm.mit.edu."
            description = request.POST['description']
            text = description + "\n\n\n\n_______________________________________________\n"+shameless_plug
            name = request.POST['name']
            thread_id = str(time.time())+"@"+MAIN_URL
            headers = [('REUSE-MOBILE', 'true'), ('Message-ID', thread_id)]

            reuse_list = [REUSE_EMAIL_ADDRESS]  # testing

            status = send_mail(sender, reuse_list, subject, text, headers)

            if status == 'success':
                location = request.POST['location']
                tags = request.POST['tags']
                new_thread = EmailThread.objects.create(subject=subject, thread_id=thread_id)
                new_email = NewPostEmail.objects.create(sender=sender, subject=subject, text=text, thread=new_thread)

                ipl = ItemPostLocator()
                data = ipl.get_location(location.upper())

                if data is not None:
                    lon = str(data['lon'])
                    lat = str(data['lat'])
                else:
                    lon = ''
                    lat = ''

                new_item = Item.objects.create(name=name, description=description, location=location, tags=tags, post_email=new_email, lat=lat, lon=lon, is_email=False, thread=new_thread)

                response = jsonpickle.encode({"success": True})
                return HttpResponse(response)
            else:

                response = jsonpickle.encode({"success": False})
                return HttpResponse(response)

        else:
            return HttpResponseForbidden("Invalid Request.")


class ThreadClaimView(AbstractThreadView):
    """This view handles claiming a reuse item.
    It sends email to reuse list on the appropriate thread.

    Expects a POST request from client as per the api
    specifications
    """

    def post(self, request, *args, **kwargs):

        client = self.authenticate_user(request, *args, **kwargs)

        if client is not None:

            if not 'item_id' in request.POST:
                return HttpResponseBadRequest("Cannot find 'item_id' attribute")

            item_id = request.POST['item_id']
            item = Item.objects.get(pk=item_id)

            if item.claimed:
                response = jsonpickle.encode({"success": False})
                return HttpResponse(response)

            subject = "Re: " + item.thread.subject
            text = "[CLAIMED!]\n\n" + item.post_email.text
            sender = client.email
            reuse_list = [REUSE_EMAIL_ADDRESS]
            thread_id = item.thread.thread_id
            msg_id = str(time.time())+"@"+MAIN_URL
            headers = [('REUSE-MOBILE', 'true'), ('Message-ID', msg_id)]

            if thread_id != '':
                headers.append(('In-Reply-To', thread_id))

            status = send_mail(sender, reuse_list, subject, text, headers)

            if status == "success":
                item.claimed = True
                item.save()

                response = jsonpickle.encode({"success": True})
                return HttpResponse(response)
            else:

                #TODO: possible log errors

                response = jsonpickle.encode({"success": False})
                return HttpResponse(response)

        else:

            return HttpResponseForbidden("Invalid Request.")