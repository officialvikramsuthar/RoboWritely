from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^blog/(?P<slug>[-\w]+)/$', views.display_blog_post, name='display_blog_post'),
    path('', views.home, name='home'),
]