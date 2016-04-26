"""gb_ips URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('api.urls')),
#    url(r'^training/', include('training.urls')),
#    url(r'^training/', include([url(r'^receive/$',views.index),url(r'^datarequest/$',views.datarequest),url(r'^result/$',views.result),url(r'^all/$',views.alldata)])),

    url(r'^receive/$','training.views.index',name='receive'),
    url(r'^datarequest/$','training.views.datarequest',name='datarequest'),
    url(r'^result/$','training.views.result',name='result'),
    url(r'^all/$','training.views.alldata',name='allresult'),
    url(r'^run/$','training.views.run',name='run'),

]
