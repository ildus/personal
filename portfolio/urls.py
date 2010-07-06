#coding:utf-8

from django.conf.urls.defaults import *
from django.conf import settings
from portfolio import views

urlpatterns = patterns('',
    (r'^$', views.solutions),
    url(r'^tag/(?P<tag>[^/]+)/$', views.solutions_by_tag, name = "ptag"),
)