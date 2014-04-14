from django.conf.urls import patterns, url

from views import ThreadGetView, ThreadPostView, ThreadClaimView, ThreadLogView

urlpatterns = patterns('',

    #direct get request to ThreadGetView
    url(r'^get/$', ThreadGetView.as_view()),

    #direct post request to ThreadPostView
    url(r'^post/$', ThreadPostView.as_view()),

    #direct claim request to ThreadClaimView
    url(r'^claim/$', ThreadClaimView.as_view()),

    #direct logging request to ThreadLogView (log client data for user testing)
    url(r'^log/$', ThreadLogView.as_view()),

)