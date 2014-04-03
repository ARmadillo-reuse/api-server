from django.conf.urls import patterns, url

from views import SignupView, VerifyView

urlpatterns = patterns('',

    #direct post request to LoginView
    url(r'^signup/$', SignupView.as_view()),

    #direct get request to VerifyView
    url(r'^verify/$', VerifyView.as_view()),


)