from django.conf.urls import url

from . import views as bucket_views

urlpatterns = [
    url(r'^$', bucket_views.index),
    url(r'^about/', bucket_views.about),
    url(r'^category/(?P<category_name_url>\w+)/$', bucket_views.category, name='category'),
    url(r'^category/$', bucket_views.category_list, name='category_list'),
    url(r'^add_category/$', bucket_views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_url>\w+)/add/$', bucket_views.add_page, name='add_page'),
    url(r'^category/(?P<category_name_url>\w+)/edit/$', bucket_views.edit_category, name='edit_category'),
    url(r'^category/(?P<category_name_url>\w+)/delete/$', bucket_views.delete_category, name='delete_category'),
    url(r'^category/(?P<category_name_url>\w+)/(?P<page_name_url>\w+)/$', bucket_views.page_detail, name='page_detail'),
    url(r'^category/(?P<category_name_url>\w+)/(?P<page_name_url>\w+)/edit$', bucket_views.edit_page, name='edit_page'),
    url(r'^category/(?P<category_name_url>\w+)/(?P<page_name_url>\w+)/delete$', bucket_views.delete_page, name='delete_page'),
    url(r'^category/(?P<category_name_url>\w+)/(?P<page_name_url>\w+)/places$', bucket_views.places_page, name='places_page'),
    ]