from django.urls import path, re_path
from .views import views

urlpatterns = [
    path('generate_content/', views.generate_content, name='generate_content'),
    re_path(r'^blog/(?P<slug>[-\w]+)/$', views.display_blog_post, name='display_blog_post'),
]