"""
URL configuration for Robowritely project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from Robowritely.sitemaps import BlogSitemap, StaticSitemap, StaticPageSitemap, StaticTechnologySitemap, StaticCountryHomeSitemap

sitemaps = {
    "blog": BlogSitemap,
    "static" :StaticSitemap,
    "static2" : StaticPageSitemap,
    "statictech":StaticTechnologySitemap,
    "home":StaticCountryHomeSitemap
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('ContentCreation.urls')),
    path("", include('PriceCompare.urls')),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap", ),
    path(r'robots.txt', TemplateView.as_view(template_name=settings.ROBOTSTXTFILENAME, content_type='text/plain')),
]



