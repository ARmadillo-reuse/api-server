from django.views.generic import View
from django.http import HttpResponse


class LoginView(View):
    """This class handles all requests from client that
    have to do with Login/Signup/Deactivate ...
    It creates the server entry for a client and establishes
    the security protocol/token on both server and client.
    """

    def get(self, request, *args, **kwargs):

        #If client is connecting for the first time,
            #set up verification link and email it to client

        #If client has been verified,
            # create token,
            # insert necessary user/device information into database
                # this may include GCM identification data for push notifications
            # send token back to client along with response

        response = "Congrats, you are now in LoginView."
        return HttpResponse(response)