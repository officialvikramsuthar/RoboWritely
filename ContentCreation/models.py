from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Paragraph(models.Model):
    blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE)
    content = RichTextField()
    image = models.ImageField(upload_to='blog/images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class BlogPost(models.Model):
    title = RichTextField()
    keyword = models.CharField(max_length=300)
    meta_description = models.CharField(max_length=300)
    paragraphs = models.ManyToManyField(Paragraph, related_name='blog_posts')
    created_at = models.DateTimeField(auto_now_add=True)