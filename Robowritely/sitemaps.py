



from django.contrib.sitemaps import Sitemap
from ContentCreation.models import *
from PriceCompare.models import DiscPrice


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
        page_name_list = ['hard_disc_price_compare', "disc_price_compare", "ssd_disc_price_compare", "compare_ssd_price", "compare-ssd-hdd-prices", "top-ssd-vs-hdd-price-guide", "ssd-hdd-price-battle", "discounted-ssd-hdd-prices","ultimate-ssd-hdd-price-check", "compare-leading-ssd-hdd-prices","ssd-hdd-cost-analysis", "budget-friendly-ssd-vs-hdd-pricing"   ]
        country_list = ["USA","IN","UK","FR","DE","CA","AU"]
        page_country_list = []

        for country in country_list:
            for page in page_name_list:
                page_country_list.append((page, country))

        return page_country_list

    def location(self, item):
        return reverse(item[0], kwargs={'country':item[1]})

class StaticPageSitemap(Sitemap):
    """Reverse 'static' views for XML sitemap."""
    changefreq = "daily"
    priority = 0.5

    def items(self):
        # Return list of url names for views to include in sitemap
        page_name_list2 = ['new_hard_disc_price_compare', "new_disc_price_compare", "new_ssd_disc_price_compare",
                           "new_compare_ssd_price", "new_compare-ssd-hdd-prices", "new_top-ssd-vs-hdd-price-guide", "new_ssd-hdd-price-battle",
                           "new_discounted-ssd-hdd-prices",
                           "new_ultimate-ssd-hdd-price-check", "new_compare-leading-ssd-hdd-prices", "new_ssd-hdd-cost-analysis",
                           "new_budget-friendly-ssd-vs-hdd-pricing"]

        country_list = ["USA","IN","UK","FR","DE","CA","AU"]
        page_country_list = []

        for country in country_list:
            for page in page_name_list2:
                page_country_list.append((page, country, "New"))
                page_country_list.append((page, country, "Used"))

        return page_country_list

    def location(self, item):
        return reverse(item[0], kwargs={'country':item[1], 'condition':item[2]})


class StaticTechnologySitemap(Sitemap):
    """Reverse 'static' views for XML sitemap."""
    changefreq = "daily"
    priority = 0.5

    def items(self):
        # Return list of url names for views to include in sitemap
        page_name_list3 = ['tech_hard_disc_price_compare', "tech_disc_price_compare", "tech_ssd_disc_price_compare",
                           "tech_compare_ssd_price", "tech_compare-ssd-hdd-prices", "tech_top-ssd-vs-hdd-price-guide", "tech_ssd-hdd-price-battle",
                           "tech_discounted-ssd-hdd-prices",
                           "tech_ultimate-ssd-hdd-price-check", "tech_compare-leading-ssd-hdd-prices", "tech_ssd-hdd-cost-analysis",
                           "tech_budget-friendly-ssd-vs-hdd-pricing"]

        country_list = ["USA","IN","UK","FR","DE","CA","AU"]
        page_country_list = []

        for country in country_list:
            for page in page_name_list3:

                tech_lis = list(DiscPrice.objects.filter(country=country).values_list("technology", flat=True).distinct())

                for tech in tech_lis:
                    page_country_list.append((page, country, tech, "New"))
                    page_country_list.append((page, country, tech, "Used"))

        return page_country_list

    def location(self, item):
        return reverse(item[0], kwargs={'country':item[1], 'technology':item[2],'condition':item[3]})