from django.conf.urls.defaults import *
from django.conf import settings
from blog import views

urlpatterns = patterns('',
    (r'^$', views.articles),
    (r'^([a-z0-9_]+)/$', views.article),
    (r'^category/([a-z0-9_]+)/$', views.category),
    (r'^comment/edit/', views.comment_edit),
    (r'^comment/(\d+)/$', views.comment),
    url(r'^tag/(?P<tag>[^/]+)/$', views.articles_by_tag, name = "blog_tag"),
)