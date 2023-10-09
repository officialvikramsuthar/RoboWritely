from django.db import models
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify


# Create your models here.
class Paragraph(models.Model):
    blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE)
    content = RichTextField()
    image = models.ImageField(upload_to='blog/images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class BlogPost(models.Model):
    title = RichTextField()
    slug = models.SlugField(max_length=100)
    heading = models.CharField(max_length=100, blank=True, null=True)
    intro = models.CharField(max_length=300, blank=True, null=True)
    keyword = models.CharField(max_length=300, blank=True, null=True)
    meta_description = models.CharField(max_length=300)
    paragraphs = models.ManyToManyField(Paragraph, related_name='blog_posts')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug)
        super(BlogPost, self).save(*args, **kwargs)