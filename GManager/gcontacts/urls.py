from django.conf.urls.defaults import patterns, url

from gcontacts import views

urlpatterns = patterns('',
    url(r'^$', views.index),
        )
