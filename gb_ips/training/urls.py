from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
#    url(r'^training/', include([url(r'^receive/$',views.index),url(r'^datarequest/$',views.datarequest),url(r'^result/$',views.result),url(r'^all/$',views.alldata)])),

    url(r'^receive/$','training.views.index',name='receive'),
    url(r'^datarequest/$','training.views.datarequest',name='datarequest'),
    url(r'^result/$','training.views.result',name='result'),
    url(r'^all/$','training.views.all',name='allresult'),

]
