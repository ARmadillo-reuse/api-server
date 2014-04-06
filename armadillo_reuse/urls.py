from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    #direct all api calls to the web_api application
    url(r'^api/', include('web_api.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
