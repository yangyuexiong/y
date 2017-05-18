
from django.conf.urls import url,include
from bbs import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^category/(\d+)/$', views.category),
    url(r'^detail/(\d+)/$', views.article_detail,name='article_detail'),
    url(r'^comment/$', views.comment,name='post_comment'),
]
