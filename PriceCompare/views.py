from django.shortcuts import render

from PriceCompare.models import DiscPrice


# Create your views here.

def get_all_discs(request):
    discs_info = list(DiscPrice.objects.all())
    context = {'disc_info': discs_info}
    return render(request, 'PriceCompare/discpricecompare.html', context)