from django.conf.urls import url
from . import views

app_name = 'peminjam'

urlpatterns = [

    # /peminjam/
    url(r'^$', views.index, name='index'),

    # /peminjam/add/
    url(r'^add/$',views.formadd, name='add'),

    # /peminjam/edit/4
    url(r'^edit/$', views.formedit, name='editbase'),
    url(r'^edit/(?P<peminjam_id>[0-9]+)/$', views.formedit, name='edit'),

    # /peminjam/delete/4
    url(r'^delete/$', views.formdelete, name='deletebase'),
    url(r'^delete/(?P<peminjam_id>[0-9]+)/$', views.formdelete, name='delete'),

    # /peminjam/fetchjson/
    url(r'^json/$', views.fetchrecord, name='json'),
]
