from django.db import models

class DiscPrice(models.Model):
    country = models.CharField(max_length=10, default="USA", blank=True)
    price_per_tb = models.CharField(max_length=255, null=True, blank=True)
    price_per_gb = models.CharField(max_length=255, null=True, blank=True)
    price = models.CharField(max_length=255, null=True, blank=True)
    capacity = models.CharField(max_length=255, null=True, blank=True)
    warranty = models.CharField(max_length=255, null=True, blank=True)
    form_factor = models.CharField(max_length=255, null=True, blank=True)
    technology = models.CharField(max_length=255, null=True, blank=True)
    condition = models.CharField(max_length=255, null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    Link = models.TextField(null=True, blank=True)
