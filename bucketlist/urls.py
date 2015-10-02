from django.conf.urls import url

from . import views as bucket_views

urlpatterns = [
    url(r'^$', bucket_views.index),
    url(r'^register/$', bucket_views.register, name='register'),
    url(r'^login/$', bucket_views.user_login, name='login'),
    url(r'^logout/$', bucket_views.user_logout, name='logout'),
    url(r'^about/$', bucket_views.about),
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