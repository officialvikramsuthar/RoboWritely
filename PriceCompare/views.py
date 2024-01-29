from django.conf import settings
from django.db.models import Q
from django.shortcuts import render

from PriceCompare.models import DiscPrice


# Create your views here.

def get_all_discs(request, country="USA", technology=None, condition=None):
    filters = Q()

    if condition:
        filters &= Q(condition=condition)

    if technology:
        filters &= Q(technology=technology)

    discs_info = list(DiscPrice.objects.filter(country=country).filter(filters).all())
    page_title = request.path.replace('-',' ').replace('/', ' ')
    page_keyword =  page_title + " product reviews, top products, buying guide, recommendations, best in class, consumer advice, hard disc, SSD, laptop, PC storage price comparision in USA, India "
    page_description = page_title + ' on our comprehensive site page. Find the best deals and make informed decisions on storage solutions tailored to your needs. Uncover the most competitive prices globally for a seamless shopping experience. '

    if technology:
        technology += " Storage Solutions "
    else:
        technology = "Storage Solutions"
    context = {'disc_info': discs_info, 'page_title':page_title, 'technology':technology, 'condition':condition, 'page_keyword' : page_keyword, "page_description" : page_description, 'country':settings.COUNTRY_LOGO_MAPPING.get(country, "us")}
    return render(request, 'PriceCompare/discpricecompare.html', context)