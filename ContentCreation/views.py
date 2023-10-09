from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import BlogPost, Paragraph


def display_blog_post(request, id,  slug):
    blog_post = get_object_or_404(BlogPost, id=id)
    paragraphs = Paragraph.objects.filter(blog_post=blog_post).all()
    context = {'blog_post': blog_post, 'paragraphs':paragraphs}
    return render(request, 'ContentCreation/blogpost.html', context)


def home(request):
    latest_blogs = BlogPost.objects.order_by('-created_at')[:10]
    context = {'latest_blogs': latest_blogs}
    return render(request, 'ContentCreation/home.html', context)