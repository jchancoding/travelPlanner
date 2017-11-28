from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration', views.registration),
    url(r'^login', views.login),
    url(r'^success', views.success),
    url(r'^delete', views.delete),
    url(r'^dashboard', views.dashboard),
    url(r'^tripgroups/(?P<url_id>\d+)/$', views.trippage),
    url(r'^tripgroups/create$', views.newtrip),
    url(r'^logout', views.logout),
    url(r'^createtrip', views.createtrip),
    url(r'^tripgroups/(?P<operation>.+)/(?P<trip_id>\d+)/$', views.change_trip)
]
