from django.db import models

# Create your models here.

class Content(models.Model):
    keywords = models.CharField(max_length=200)
    heading = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)