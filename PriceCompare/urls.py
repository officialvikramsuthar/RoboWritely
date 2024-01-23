from django.urls import path, re_path
from . import views
urlpatterns1 = [
    path('<country>/hard-disc-price-comparision/', views.get_all_discs, name="hard_disc_price_compare"),
    path('<country>/disc-price-comparion/', views.get_all_discs, name="disc_price_compare"),
    path('<country>/ssd-price-comparision/', views.get_all_discs, name="ssd_disc_price_compare"),
    path('<country>/best-ssd-hard-disk-deals', views.get_all_discs, name="compare_ssd_price"),
    path('<country>/compare-ssd-hdd-prices', views.get_all_discs, name="compare-ssd-hdd-prices"),
    path('<country>/top-ssd-vs-hdd-price-guide', views.get_all_discs, name="top-ssd-vs-hdd-price-guide"),
    path('<country>/top-ssd-vs-hdd-price-guide', views.get_all_discs, name="top-ssd-vs-hdd-price-guide"),
    path('<country>/ssd-hdd-price-battle', views.get_all_discs, name="ssd-hdd-price-battle"),
    path('<country>/discounted-ssd-hdd-prices', views.get_all_discs, name="discounted-ssd-hdd-prices"),
    path('<country>/ultimate-ssd-hdd-price-check', views.get_all_discs, name="ultimate-ssd-hdd-price-check"),
    path('<country>/compare-leading-ssd-hdd-prices', views.get_all_discs, name="compare-leading-ssd-hdd-prices"),
    path('<country>/ssd-hdd-cost-analysis', views.get_all_discs, name="ssd-hdd-cost-analysis"),
    path('<country>/budget-friendly-ssd-vs-hdd-pricing', views.get_all_discs, name="budget-friendly-ssd-vs-hdd-pricing"),
]


urlpatterns2 = [
    path('<country>/hard-disc-price-comparision/<str:condition>/', views.get_all_discs, name="new_hard_disc_price_compare"),
    path('<country>/disc-price-comparion/<str:condition>/', views.get_all_discs, name="new_disc_price_compare"),
    path('<country>/ssd-price-comparision/<str:condition>/', views.get_all_discs, name="new_ssd_disc_price_compare"),
    path('<country>/best-ssd-hard-disk-deals/<str:condition>/', views.get_all_discs, name="new_compare_ssd_price"),
    path('<country>/compare-ssd-hdd-prices/<str:condition>/', views.get_all_discs, name="new_compare-ssd-hdd-prices"),
    path('<country>/top-ssd-vs-hdd-price-guide/<str:condition>/', views.get_all_discs, name="new_top-ssd-vs-hdd-price-guide"),
    path('<country>/top-ssd-vs-hdd-price-guide/<str:condition>/', views.get_all_discs, name="new_top-ssd-vs-hdd-price-guide"),
    path('<country>/ssd-hdd-price-battle/<str:condition>/', views.get_all_discs, name="new_ssd-hdd-price-battle"),
    path('<country>/discounted-ssd-hdd-prices<str:condition>/', views.get_all_discs, name="new_discounted-ssd-hdd-prices"),
    path('<country>/ultimate-ssd-hdd-price-check/<str:condition>/', views.get_all_discs, name="new_ultimate-ssd-hdd-price-check"),
    path('<country>/compare-leading-ssd-hdd-prices/<str:condition>/', views.get_all_discs, name="new_compare-leading-ssd-hdd-prices"),
    path('<country>/ssd-hdd-cost-analysis/<str:condition>/', views.get_all_discs, name="new_ssd-hdd-cost-analysis"),
    path('<country>/budget-friendly-ssd-vs-hdd-pricing/<str:condition>/', views.get_all_discs, name="new_budget-friendly-ssd-vs-hdd-pricing"),
]

urlpatterns3 = [
    path('<country>/hard-disc-price-comparision/<str:technology>/<str:condition>/', views.get_all_discs, name="tech_hard_disc_price_compare"),
    path('<country>/disc-price-comparion/<str:technology>/<str:condition>/', views.get_all_discs, name="tech_disc_price_compare"),
    path('<country>/ssd-price-comparision/<str:technology>/<str:condition>/', views.get_all_discs, name="tech_ssd_disc_price_compare"),
    path('<country>/best-ssd-hard-disk-deals/<str:technology>/<str:condition>/', views.get_all_discs, name="tech_compare_ssd_price"),
    path('<country>/compare-ssd-hdd-prices/<str:technology>/<str:condition>/', views.get_all_discs, name="tech_compare-ssd-hdd-prices"),
    path('<country>/top-ssd-vs-hdd-price-guide/<str:technology>/<str:condition>/', views.get_all_discs, name="tech_top-ssd-vs-hdd-price-guide"),
    path('<country>/top-ssd-vs-hdd-price-guide/<str:technology>/<str:condition>/', views.get_all_discs, name="tech_top-ssd-vs-hdd-price-guide"),
    path('<country>/ssd-hdd-price-battle/<str:technology>/<str:condition>/', views.get_all_discs, name="tech_ssd-hdd-price-battle"),
    path('<country>/discounted-ssd-hdd-prices/<str:technology>/<str:condition>/', views.get_all_discs, name="tech_discounted-ssd-hdd-prices"),
    path('<country>/ultimate-ssd-hdd-price-check/<str:technology>/<str:condition>/', views.get_all_discs, name="tech_ultimate-ssd-hdd-price-check"),
    path('<country>/compare-leading-ssd-hdd-prices/<str:technology>/<str:condition>/', views.get_all_discs, name="tech_compare-leading-ssd-hdd-prices"),
    path('<country>/ssd-hdd-cost-analysis/<str:technology>/<str:condition>/', views.get_all_discs, name="tech_ssd-hdd-cost-analysis"),
    path('<country>/budget-friendly-ssd-vs-hdd-pricing/<str:technology>/<str:condition>/', views.get_all_discs, name="tech_budget-friendly-ssd-vs-hdd-pricing"),
]

urlpatterns = urlpatterns1 + urlpatterns2 + urlpatterns3