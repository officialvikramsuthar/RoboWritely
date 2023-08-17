from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Content

def display_blog_post(request, slug):
    blog_post = get_object_or_404(Content, slug=slug)
    context = {'blog_post': blog_post}
    return render(request, 'ContentCreation/blogpost.html', context)


def home(request):
    latest_blogs = Content.objects.order_by('-timestamp')[:10]
    context = {'latest_blogs': latest_blogs}
    return render(request, 'ContentCreation/home.html', context)