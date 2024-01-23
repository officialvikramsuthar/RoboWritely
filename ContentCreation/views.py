
from django.shortcuts import render, get_object_or_404
from django.urls import get_resolver, reverse
from PriceCompare.models import DiscPrice
from .models import BlogPost, Paragraph


def display_blog_post(request, id,  slug):
    blog_post = get_object_or_404(BlogPost, id=id)
    paragraphs = Paragraph.objects.filter(blog_post=blog_post).all()
    context = {'blog_post': blog_post, 'paragraphs':paragraphs}
    return render(request, 'ContentCreation/blogpost.html', context)

def generate_country_urls(country_list=[]):
    # Create a list of URLs for each country
    country_list = ["USA", "IN", "UK", "FR", "DE", "CA", "AU"]
    page_name_list = ['hard_disc_price_compare', "disc_price_compare", "ssd_disc_price_compare",
                      "compare_ssd_price", "compare-ssd-hdd-prices", "top-ssd-vs-hdd-price-guide", "ssd-hdd-price-battle", "discounted-ssd-hdd-prices",
                      "ultimate-ssd-hdd-price-check", "compare-leading-ssd-hdd-prices", "ssd-hdd-cost-analysis", "budget-friendly-ssd-vs-hdd-pricing"]

    page_name_list2 = ['new_hard_disc_price_compare', "new_disc_price_compare", "new_ssd_disc_price_compare",
                      "new_compare_ssd_price", "new_compare-ssd-hdd-prices", "new_top-ssd-vs-hdd-price-guide", "new_ssd-hdd-price-battle", "new_discounted-ssd-hdd-prices",
                      "new_ultimate-ssd-hdd-price-check", "new_compare-leading-ssd-hdd-prices", "new_ssd-hdd-cost-analysis", "new_budget-friendly-ssd-vs-hdd-pricing"]

    page_name_list3 = ['tech_hard_disc_price_compare', "tech_disc_price_compare", "tech_ssd_disc_price_compare",
                       "tech_compare_ssd_price", "tech_compare-ssd-hdd-prices", "tech_top-ssd-vs-hdd-price-guide", "tech_ssd-hdd-price-battle",
                       "tech_discounted-ssd-hdd-prices",
                       "tech_ultimate-ssd-hdd-price-check", "tech_compare-leading-ssd-hdd-prices", "tech_ssd-hdd-cost-analysis", "tech_budget-friendly-ssd-vs-hdd-pricing"]
    urls = []

    for country in country_list:
        for page in page_name_list:
            kwargs =  {'country':country}
            url = reverse(page, kwargs=kwargs)
            name = url.replace("-"," ").replace("/"," ").upper()
            urls.append((name, url))

    for country in country_list:
        for page in page_name_list3:
            tech_lis = list(DiscPrice.objects.filter(country=country).values_list("technology", flat=True).distinct())

            for tech in tech_lis:

                kwargs = {'country': country, 'technology':tech, 'condition':"New"}
                url = reverse(page, kwargs=kwargs)
                name = url.replace("-", " ").replace("/", " ").upper()
                urls.append((name, url))

                kwargs = {'country': country, 'technology':tech, 'condition': "Used"}
                url = reverse(page, kwargs=kwargs)
                name = url.replace("-", " ").replace("/", " ").upper()
                urls.append((name, url))

    for country in country_list:

        for page in page_name_list2:

            kwargs = {'country': country, 'condition': "New"}
            url = reverse(page, kwargs=kwargs)
            name = url.replace("-", " ").replace("/", " ").upper()
            urls.append((name, url))

            kwargs = {'country': country, 'condition': "Used"}
            url = reverse(page, kwargs=kwargs)
            name = url.replace("-", " ").replace("/", " ").upper()
            urls.append((name, url))

    return list(set(urls))

def home(request):


    urls = generate_country_urls()
    context ={'urls':urls}

    return render(request, 'ContentCreation/home.html', context)