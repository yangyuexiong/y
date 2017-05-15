
from django.conf.urls import url,include
from bbs import views

urlpatterns = [
    url(r'^$', views.index),
]
