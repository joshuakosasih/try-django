from django.conf.urls import url
from . import views

app_name = 'ruangan'

urlpatterns = [

    # /ruangan/
    url(r'^$', views.index, name='index'),

    # /ruangan/add/
    url(r'^add/$', views.formadd, name='add'),

    # /ruangan/edit/4
    url(r'^edit/$', views.formedit, name='editbase'),
    url(r'^edit/(?P<ruangan_id>[0-9]+)/$', views.formedit, name='edit'),

    # /ruangan/delete/4
    url(r'^delete/$', views.formdelete, name='deletebase'),
    url(r'^delete/(?P<ruangan_id>[0-9]+)/$', views.formdelete, name='delete'),

    # /ruangan/json/
    url(r'^json/$', views.fetchrecord, name='json'),

    # /ruangan/json_umum/
    url(r'^json_umum/$', views.fetchrecord_umum, name='json_umum'),
]
