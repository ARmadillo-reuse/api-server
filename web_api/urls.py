from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    #direct request to be handled by the LoginView class
    url(r'^login/', include('login.urls')),

    #GET request for an updated database of items
    #direct request to be handled by the ThreadView class
    url(r'^thread/', include('threads.urls')),

)