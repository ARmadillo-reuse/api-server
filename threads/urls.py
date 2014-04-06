from django.conf.urls import patterns, url

from views import ThreadGetView, ThreadPostView, ThreadClaimView

urlpatterns = patterns('',

    #direct get request to ThreadGetView
    url(r'^get/$', ThreadGetView.as_view()),

    #direct post request to ThreadPostView
    url(r'^post/$', ThreadPostView.as_view()),

    #direct claim request to ThreadClaimView
    url(r'^claim/$', ThreadClaimView.as_view()),

)