# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns, include
#from django.template.base import Context #Template, RequestContext  # Library, Node
#from django.views.generic import ListView

#from customers.models import CustomerImage, Testimonial


urlpatterns = patterns('customers.views',
    #(r'^', 'test'),

    url (r'^$',             'index', name='customers'),
    url (r'^save_email/$',  'save_email'),
    url (r'^emails/$',      'emails'),
)
