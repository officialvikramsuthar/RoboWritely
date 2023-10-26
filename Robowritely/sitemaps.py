



from django.contrib.sitemaps import Sitemap
from ContentCreation.models import *


class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return BlogPost.objects.all()

    def lastmod(self, obj):
        return obj.created_at