from django.urls import path, re_path
from . import views

urlpatterns = [
    path('blog/<id>/<slug>', views.display_blog_post, name='display_blog_post'),
    path('', views.home, name='home'),
]