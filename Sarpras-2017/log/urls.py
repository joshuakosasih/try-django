from django.conf.urls import url
from . import views

app_name = 'log'

urlpatterns = [

    # /log/
    url(r'^$', views.index, name='index'),

    # /log/json/2016/
    url(r'^json/$', views.fetchrecord, name='jsonbase'),
    url(r'^json/(?P<start_year>[0-9]+)/$', views.fetchrecord, name='json'),

    # /log/filter/2017/1
    url(r'^filter/$', views.filter, name='filterbase'),
    url(r'^filter/(?P<select_year>[0-9]+)/(?P<select_month>[0-9]+)/', views.filter, name='filter'),
]
