from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^rps_pos/$', 'api.views.rps_pos'),
]
