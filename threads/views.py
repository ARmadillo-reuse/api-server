from django.views.generic import View
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from web_api.models import *
from django.contrib.auth.models import User
import jsonpickle
from django.core import serializers
from django.core.mail import send_mail
from armadillo_reuse.settings import REUSE_EMAIL_ADDRESS


class AbstractThreadView(View):
    """ A base class for all Thread handler views.
    """
    def authenticate_user(self, request, *args, **kwargs):
        """Authenticates user and if it is a valid request,
        identifies and returns the client's User object

        Returns None if authentication fails for whatever reason
        """
        return User.objects.all()[0]


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

            attributes = ['subject', 'text', 'name']
            for attribute in attributes:
                if not attribute in request.POST:
                    return HttpResponseBadRequest("Cannot find '%s' attribute" % attribute)

            subject = request.POST['subject']
            sender = client.email
            text = request.POST['text']
            name = request.POST['name']

            new_thread = EmailThread.objects.create(subject=subject)
            new_email = NewPostEmail.objects.create(sender=sender, subject=subject, text=text, thread=new_thread)
            new_item = Item.objects.create(name=name, post_email=new_email, thread=new_thread)

            reuse_list = [REUSE_EMAIL_ADDRESS]  # testing

            send_mail(subject, text, sender, reuse_list, fail_silently=False)
            response = jsonpickle.encode({"success": True, "item":new_item.name})
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
                response = jsonpickle.encode({"success": False, "item": item.name})
                return HttpResponse(response)

            item.claimed = True
            item.save()

            subject = "Re: " + item.thread.subject + " [CLAIMED]"
            text = "ITEM HAS BEEN CLAIMED!\n\n" + item.post_email.text
            sender = client.email
            reuse_list = [REUSE_EMAIL_ADDRESS]

            send_mail(subject, text, sender, reuse_list, fail_silently=False)
            response = jsonpickle.encode({"success": True, "item": item.name})
            return HttpResponse(response)
        else:
            return HttpResponseForbidden("Invalid Request.")