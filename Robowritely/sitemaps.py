



from django.contrib.sitemaps import Sitemap
from ContentCreation.models import *


class BlogSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return BlogPost.objects.all()

    def lastmod(self, obj):
        return obj.created_at

class StaticSitemap(Sitemap):
    """Reverse 'static' views for XML sitemap."""
    changefreq = "daily"
    priority = 0.5

    def items(self):
        # Return list of url names for views to include in sitemap
        return ['hard_disc_price_compare', "disc_price_compare", "ssd_disc_price_compare", "ssd_disc_price_compare_usa", "hdd_price_compare_usa", "compare_ssd_price", "compare-ssd-hdd-prices", "top-ssd-vs-hdd-price-guide", "ssd-hdd-price-battle", "discounted-ssd-hdd-prices","ultimate-ssd-hdd-price-check", "compare-leading-ssd-hdd-prices","ssd-hdd-cost-analysis", "budget-friendly-ssd-vs-hdd-pricing"   ]

    def location(self, item):
        return reverse(item)