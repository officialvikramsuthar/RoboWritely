from django.urls import path, re_path
from . import views

urlpatterns = [
    path('hard-disc-price-comparision', views.get_all_discs, name="hard_disc_price_compare"),
    path('disc-price-comparion', views.get_all_discs, name="disc_price_compare"),
    path('ssd-price-comparision', views.get_all_discs, name="ssd_disc_price_compare"),
    path('ssd-price-comparision-usa', views.get_all_discs, name="ssd_disc_price_compare_usa"),
    path('compare-hdd-price-usa', views.get_all_discs,  name="hdd_price_compare_usa"),
    path('best-ssd-hard-disk-deals', views.get_all_discs, name="compare_ssd_price"),
    path('compare-ssd-hdd-prices', views.get_all_discs, name="compare-ssd-hdd-prices"),
    path('top-ssd-vs-hdd-price-guide', views.get_all_discs, name="top-ssd-vs-hdd-price-guide"),
    path('top-ssd-vs-hdd-price-guide', views.get_all_discs, name="top-ssd-vs-hdd-price-guide"),
    path('ssd-hdd-price-battle', views.get_all_discs, name="ssd-hdd-price-battle"),
    path('discounted-ssd-hdd-prices', views.get_all_discs, name="discounted-ssd-hdd-prices"),
    path('ultimate-ssd-hdd-price-check', views.get_all_discs, name="ultimate-ssd-hdd-price-check"),
    path('compare-leading-ssd-hdd-prices', views.get_all_discs, name="compare-leading-ssd-hdd-prices"),
    path('ssd-hdd-cost-analysis', views.get_all_discs, name="ssd-hdd-cost-analysis"),
    path('budget-friendly-ssd-vs-hdd-pricing', views.get_all_discs, name="budget-friendly-ssd-vs-hdd-pricing"),
]
