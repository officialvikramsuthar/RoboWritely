from django.shortcuts import render

from PriceCompare.models import DiscPrice


# Create your views here.

def get_all_discs(request, country="USA"):
    discs_info = list(DiscPrice.objects.filter(country=country).all())
    context = {'disc_info': discs_info}
    return render(request, 'PriceCompare/discpricecompare.html', context)