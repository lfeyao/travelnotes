from django.conf.urls import url

from . import views as bucket_views

urlpatterns = [
    url(r'^$', bucket_views.index),
    url(r'^about/', bucket_views.about),
    url(r'^add_category/$', bucket_views.add_category, name='add_category'),
    url(r'^add_page/$', bucket_views.add_page, name='add_page'),
    url(r'^category/(?P<category_name_url>\w+)/$', bucket_views.category, name='category'), 
]