from django.conf.urls import url

from . import views as mainviews

urlpatterns = [
    url(r'^$', mainviews.homepage),
]