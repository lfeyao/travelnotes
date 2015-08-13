from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'author/get_name/$', views.get_name, name='get_name'),
    url(r'^add_name/$', views.add_name, name='add_name'),
    url(r'author/$', views.author, name='author'),
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    #url(r'^add_Question', views.add_Question),
]