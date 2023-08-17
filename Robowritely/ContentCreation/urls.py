from django.urls import path, re_path
from .views import display_blog_post

urlpatterns = [
    re_path(r'^blog/(?P<slug>[-\w]+)/$', display_blog_post, name='display_blog_post'),
]