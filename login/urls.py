from django.conf.urls import patterns, url

from views import SignupView, VerifyView, UnregisterView

urlpatterns = patterns('',

    #direct post request to SignupView
    url(r'^signup/$', SignupView.as_view()),

    #direct get request to VerifyView
    url(r'^verify/$', VerifyView.as_view()),

    #direct post request to UnregisterView
    url(r'^unregister/$', UnregisterView.as_view()),


)