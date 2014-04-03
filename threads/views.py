from django.views.generic import View
from django.http import HttpResponse


class ThreadGetView(View):
    """This view handles client requests to get an
    update of all items that have been modified
    since the specified time as per client's request

    It queries and fetches data from database.

    Expects get request from client as per the api
    specifications.
    """

    def get(self, request, *args, **kwargs):

        #Verify request validity and identify client

        #retrive the 'after' date as specified in the get request

        #query database to find all items that have been modified since 'after'

        #send the retrieved list of items to client appropriately in JSON

        response = "I'm sending you a list of items that have been modified since " + request.GET['after']
        return HttpResponse(response)


class ThreadPostView(View):
    """This view handles posting an new item
    into the system. It retrieves data from the request
    and creates a new thread and inserts an item into
    the appropriate place in database.
    It also sends an email to the reuse list for the post.

    Expects a post request from client as per the api
    specifications
    """

    def post(self, request, *args, **kwargs):

        #Verify request validity and identify client

        #extract data from request.POST and create item to be posted

        #create a new thread and add item to the thread and insert it
        #into database

        #send out email to the reuse list

        #send push notifications as necessary (may not be per each post).

        #send success/failure notification JSON to client

        response = "Wohoo, you're item has been posted. Yaay. "
        return HttpResponse(response)


class ThreadClaimView(View):
    """This view handles claiming a reuse item.
    It sends email to reuse list on the appropriate thread.

    Expects a post request from client as per the api
    specifications
    """

    def post(self, request, *args, **kwargs):

        #Verify request validity and identify client

        #identify item to be claimed from request.POST

        #validate claim

        #make the necessary modifications in the database

        #send out email to the reuse list about claim on the appropriate thread

        #send push notifications as necessary (may not be per each post).

        #send success/failure notification JSON to client

        response = "You got it! Claimed! You now own 'Electronics Cruft'"
        return HttpResponse(response)