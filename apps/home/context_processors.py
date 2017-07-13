"""
Context processors for the Home app, which include login / registration via Userena.

These return dictionaries to be merged into a
template context. Each function takes the request object as its only parameter
and returns a dictionary to add to the context.

Google Analytics added 11/2015 JJW

These are referenced from the setting TEMPLATE_CONTEXT_PROCESSORS and used by
RequestContext.
"""

import random
import time

from django.conf import settings
#from django.db.models import get_models, Manager
from django.utils.safestring import mark_safe

from userena.forms import SignupForm, AuthenticationForm


#### module globals

trace = 0


#### Context Processors

def registration_forms (request):
    return {
        'signup_form': SignupForm,
        'signin_form': AuthenticationForm,
    }


def cart_variables (request):
    from helpers import SessionHelper

    seshelp = SessionHelper (request.session)
    totqty, grandtot = seshelp.cart_totals()

    return {
        'cart_totqty': totqty,
        'cart_grandtot': grandtot,
    }


def environment (request):
    import os
    return os.environ


# See https://djangosnippets.org/snippets/2338/

def google_analytics_tags (request):
  """Gets a chunk of HTML which will track Google Analytics using the current
  version of the JavaScript, alongside a noscript version."""

  web_property_id = getattr(settings, 'GOOGLE_ANALYTICS_ID', False)
  domain = getattr(settings, 'GOOGLE_ANALYTICS_DOMAIN', False)

  if not web_property_id or not domain:
    return { 'google_analytics': '<!-- Set GOOGLE_ANALYTICS_ID and GOOGLE_ANALYTICS_DOMAIN to include Google Analytics tracking.' }

  #if getattr(settings, 'DEBUG', True):
  #  return { 'google_analytics': '<!-- Set DEBUG to False to include Google Analytics tracking.' }

  if (request.META.has_key('HTTP_REFERER') and request.META['HTTP_REFERER'] != ''):
    http_referer = request.META['HTTP_REFERER']
  else:
    http_referer = '-'

  vars = {
      'id': web_property_id,
      'domain': domain,
      'utmn': random.randint(1000000000, 9999999999),
      'cookie': random.randint(10000000, 99999999),
      'random': random.randint(1000000000, 2147483647),
      'today': str(int(time.time())),
      'referer': http_referer,
      'uservar': '-',
      'utmp': '/nojs' + request.path,
  }

  script_section = ('<script type="text/javascript">var _gaq = _gaq || []; '
      '_gaq.push([\'_setAccount\', \'%(id)s\']); '
      '_gaq.push([\'_setDomainName\', \'.%(domain)s\']); '
      '_gaq.push([\'_trackPageview\']); '
      '(function() { var ga = document.createElement(\'script\'); '
      'ga.type = \'text/javascript\'; ga.async = true; '
      'ga.src = (\'https:\' == document.location.protocol ? '
      '\'https://ssl\' : \'http://www\') + \'.google-analytics.com/ga.js\'; '
      'var s = document.getElementsByTagName(\'script\')[0]; '
      's.parentNode.insertBefore(ga, s); })(); </script>') % vars

  noscript_section = ('<noscript>'
      '<img src="//www.google-analytics.com/__utm.gif?utmwv=3&utmn='
      '%(utmn)s&utme=&utmcs=-&utmsr=-&utmsc=-&utmul=-&utmje=0&utmfl=-&utmdt=-'
      '&utmhn=%(domain)s&utmhid=%(utmn)s&utmr=%(referer)s&utmp=%(utmp)s'
      '&utmac=%(id)s&utmcc=__utma%%3D%(cookie)s.%(random)s.%(today)s.'
      '%(today)s.%(today)s.2%%3B%%2B__utmz%%3D%(cookie)s.%(today)s.2.2.'
      'utmcsr%%3D_SOURCE_%%7Cutmccn%%3D_CAMPAIGN_%%7Cutmcmd%%3D_MEDIUM_%%7'
      'Cutmctr%%3D_KEYWORD_%%7Cutmcct%%3D_CONTENT_%%3B%%2B__utmv%%3D'
      '%(cookie)s.%(uservar)s%%3B;" border="0" /></noscript>') % vars

  tags = script_section + noscript_section
  return { 'google_analytics': mark_safe (tags) }
