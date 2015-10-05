# mysite URL Configuration

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/1.8/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
# Including another URLconf
#     1. Add an import:  from blog import urls as blog_urls
#     2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))

from django.conf.urls import include, url
from django.contrib import admin
from bucketlist import views as bucket_views

urlpatterns = [
    url(r'^$', bucket_views.index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/$', bucket_views.register, name='register'),
    url(r'^login/$', bucket_views.user_login, name='login'),
    url(r'^logout/$', bucket_views.user_logout, name='logout'),
    url(r'^add/$', bucket_views.add_page, name='add_page'),
    url(r'^category/add/$', bucket_views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_url>\w+)/$', bucket_views.category, name='category'),
    url(r'^category/(?P<category_name_url>\w+)/add/$', bucket_views.add_page, name='add_page'),
    url(r'^category/(?P<category_name_url>\w+)/edit/$', bucket_views.edit_category, name='edit_category'),
    url(r'^category/(?P<category_name_url>\w+)/(?P<page_name_url>\w+)/$', bucket_views.page_detail, name='page_detail'),
    url(r'^category/(?P<category_name_url>\w+)/(?P<page_name_url>\w+)/add$', bucket_views.add_place, name='add_place'),
    url(r'^category/(?P<category_name_url>\w+)/(?P<page_name_url>\w+)/edit$', bucket_views.edit_page, name='edit_page'),
    url(r'^category/(?P<category_name_url>\w+)/(?P<page_name_url>\w+)/delete$', bucket_views.delete_page, name='delete_page'),
    url(r'^category/(?P<category_name_url>\w+)/(?P<page_name_url>\w+)/(?P<direction>up|down)vote/?$', bucket_views.vote_page, name="vote_page"),
    url(r'^category/(?P<category_name_url>\w+)/(?P<page_name_url>\w+)/(?P<place_id>[0-9]+)/$', bucket_views.edit_place, name='edit_place'),
    url(r'^category/(?P<category_name_url>\w+)/(?P<page_name_url>\w+)/(?P<place_id>[0-9]+)/delete$', bucket_views.delete_place, name='delete_place'),
    url(r'^category/(?P<category_name_url>\w+)/(?P<page_name_url>\w+)/(?P<place_id>[0-9]+)/(?P<direction>up|down)vote/?$', bucket_views.vote_place, name="vote_place"),
]
