from django.conf.urls import patterns, include, url

from login.views import LoginView

urlpatterns = patterns('',

    #direct request to be handled by the LoginView class
    url(r'^login/$', LoginView.as_view()),

    #GET request for an updated database of items
    #direct request to be handled by the ThreadView class
    url(r'^thread/', include('threads.urls')),

)