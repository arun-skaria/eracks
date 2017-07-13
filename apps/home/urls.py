# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns, include
from django.template.base import Context #Template, RequestContext  # Library, Node
#from django.views.generic import ListView
from django.contrib.sitemaps.views import sitemap
from .sitemaps import all_sitemaps, partial_sitemaps


# Add this to base urls with r"'^' - JJW

urlpatterns = patterns('',
    url(r'^$', 'home.views.index', name='index'),
    url(r'^contact/$', 'home.views.contact', name='contact'),
    url(r'^testresults/$', 'home.views.testresults', name='testresults'),
    # commented social auth
    # url(r'^/register/token/(?P<backend>[^/]+)/$', 'home.views.testing_social_auth_by_access_token' , name='testing_social_auth_by_access_token'),    

    ## Sitemaps per Absolute SEO - Satish

    url(r'^sitemap\.xml$',  sitemap, dict (sitemaps=all_sitemaps,     template_name='xml_sitemap.html'),  name='xml_sitemap'),
    url(r'^ror\.xml$',      sitemap, dict (sitemaps=partial_sitemaps,     template_name='ror_sitemap.html'),  name='ror_sitemap'),
    url(r'^sitemap\.html$', sitemap, dict (sitemaps=partial_sitemaps, template_name='html_sitemap.html'), name='html_sitemap'),
)
