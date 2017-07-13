# -*- coding: utf-8 -*-

import os

try:
    import json
except ImportError:
    import simplejson as json

from django import forms
#from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext  # Template, Context,
from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify
from django.conf import settings
#from django.contrib.sitemaps import Sitemap
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

from utils import minitags as tags
from utils import Breadcrumb
from home.helpers import SessionHelper, Prod
from home.views import create_new_user
from orders.views import add_to_cart
from products.models import Product, Categories
from quotes.models import Quote,QuoteLineItem #, QuoteLineItem
from customers.models import Customer
from home.models import IpAddress
from utils.splituser import get_first_name, get_last_name
from django.utils.html import strip_tags
from django.db import IntegrityError
import datetime
import re


#### Globals and utility functions

trace = 1

product_breadcrumb = Breadcrumb ('Products', 'eRacks Products', '/products/')

#@cache_function
def product_photos (product):
    return product.images.published()  #### HERE - either return just the fname tail, or change the template!

    # see also scripts/photos/import_photos for a smarter algorithm, and brahms too :)
    # but now, we just use the DB
    folder = os.path.join (settings.STATIC_ROOT, 'images','products', product.slug)
    try:
        #return os.listdir (folder)
        return  [f for f in os.listdir (folder)
                  if os.path.isfile (os.path.join (folder, f))
                  and os.stat (os.path.join (folder, f)).st_size > 22000  # TODO: check here for in images and unpublished
                ]
    except Exception, e:
        if trace: print e
        return []


#### Quote email template

# quote_cart_request_email_template = '''
# {s.HOST_NAME} Quote Request:

# Dear {u} (eMail: {u.email}),

# You have requested a quote - a summary of your quote request is attached.

# An eRacks representative will get back to you shortly with your private online quote.

# Best regards,
# eRacks Systems

# '''

quote_product_request_email_template = '''
{s.HOST_NAME} Quote Request:

Dear {dear} (eMail: {u.email}),

You have requested a product quote for: {p.name}

Options and Choices:

{p.options_choices_as_txt}

Notes: {notes}

Base price: ${p.baseprice:.2f}
Price with requested configuration: ${p.totprice:.2f}
Shipping Weight: {p.weight} lbs

An eRacks representative will get back to you shortly with your private online quote.

Best Regards,
eRacks Systems

'''

#### description formate for QuoteLineItem
quote_requested_product_configuration = '''
{s.HOST_NAME} Quote Request:
requested product quote for: {p.name}
Options and Choices:
{p.options_choices_as_txt}
Notes: {p.notes}
Base price: ${p.baseprice:.2f}
Price with requested configuration: ${p.totprice:.2f}
Shipping Weight: {p.weight} lbs
'''
#### Get-a-Quote related

def send_quote_email (req, user, notes=""):
  ses = req.session
  seshelp = SessionHelper (ses)
  seshelp.update (req, called_from_cart=True)
  prod = Prod(ses.get ('prod', None))
  dear = user.first_name or user.email
  notes = notes + (('\n\n' + prod.notes) if prod.notes else "")

  text = quote_product_request_email_template.format (dear=dear, u=user, s=settings, p=prod, notes=notes)

  # these lines add to cart before sending it - use with other template above, call from cart page:
  #html = '<html><body>%s</body></html>' % render_to_string ('_final_cart.html', context_instance=ctx)
  #ses ['cart'] = ses.get ('cart', []) + [prod]
  #ses ['prod'] = {}
  #html = seshelp.cart_details()
  #print 'SESHELP', seshelp.cart_summary(), seshelp.cart_details()

  quote_email_list = [user.email] + settings.ORDER_EMAIL
  msg = EmailMultiAlternatives ('Your %s eracks quote request' % settings.HNN[0],
      text,  # nope: '',  # let's try attaching the text,
      settings.ORDER_FROM_EMAIL,
      quote_email_list
  )

  #msg.attach_alternative (html, "text/html")
  msg.send()


def emailForm (req, product):  # inner form to access request
    class EmailForm(forms.Form):
        name         = forms.CharField  (label='Name',  max_length=50,  required=False)  #widget=forms.TextInput (attrs=dict(style='margin-left:10px')))
        email        = forms.EmailField (label='eMail', max_length=128, required=False)
        
        def __init__(self, *args, **kwargs):
            kwargs.setdefault('label_suffix', ' :')
            super(EmailForm, self).__init__(*args, **kwargs)
            #self.label_suffix = ":   "  # nope, spaces don't work, and &nbsp; is escaped by Django :-( JJW


        def clean(self):
            cleaned_data = super(EmailForm, self).clean()
            email = cleaned_data.get("email")
            name = cleaned_data.get("name")
            quote_details = req.POST.get("notes")
            unique_initial = ""
            if (not req.user.is_authenticated() and not name and not email):
                raise forms.ValidationError ("You must either be logged in, or enter your name and email address and quote details to receive your quote.")

            if email:
                users = User.objects.filter(email__iexact=email)

                try:
                    first_name, last_name = name.split (" ", 1) # if name else (None, None)
                except ValueError:
                    first_name = ""
                    last_name = ""

                if users:
                    user = users[0]
                    first_name = user.first_name
                    last_name = user.last_name
                    if first_name and last_name:
                        name = first_name + ' ' + last_name
                
                else:
                    user, pw = create_new_user (self, req, first_name=first_name, last_name=last_name)
            else:
                user = req.user
                first_name = user.first_name
                last_name = user.last_name
                if first_name and last_name :
                    name = first_name + ' ' + last_name


            # Get product-object
            ses = req.session
            prod = ses.get ('prod', None)


            # Get product-primary-image
            image_obj = product.image
            if image_obj:
                image_url = image_obj.image.url
                image_url = re.sub(r'/media/', '', image_url)
            else:
                image_url = ""


            # Get ipaddress
            try:
                x_forwarded_for = req.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ipaddress = x_forwarded_for.split(',')[-1].strip()
                else:
                    ipaddress = req.META.get('REMOTE_ADDR')
            except Exception as e:
                if trace: print 'Exception:', e
                pass


            # Save Draft quote
            super_usr = User.objects.filter (username="joe", is_superuser=True) [0]  # Assign all quotes to Joe, for now

            if first_name and last_name:
                initial_name = first_name[0] + last_name[0]
                unique_initial = first_name[1] + last_name[1]
            else:
                initial_name = user.username[:2]
                unique_initial = user.username[-2:]

            initial_name = initial_name.upper()
            unique_initial = unique_initial.upper()
            

            customer_reference = "eRacks/%s for %s" % (product.sku, name or user.username)
            product_refrence = "eRacks/%s" % product.sku

            date_format = datetime.datetime.now().strftime("%m%d%y")
            quote_number_n = "%s-%s" %(date_format,initial_name)

            if ipaddress:
                quote_req_ip = "Quote request from IP-Address:%s" %ipaddress
            else:
                quote_req_ip = ""

            cust = Customer.objects.filter (user=user)
            if cust:
                cust = cust[0]
                
            #for unique quotenumber
            try:
                quote_obj, created = Quote.objects.get_or_create (customer=cust, shipping=0, target=0, quote_number=quote_number_n)
            except IntegrityError:
                #if quotenumber already exist changing quotenumber for new quote request:
                quote_number_n = "%s-%s-%s" %(date_format,initial_name,unique_initial)
                quote_obj, created = Quote.objects.get_or_create (customer=cust, shipping=0, target=0, quote_number=quote_number_n)
                
            quote_obj.approved_by = super_usr
            quote_obj.customer_reference = customer_reference
            quote_obj.comments = quote_req_ip
            quote_obj.image = image_url
            quote_obj.save()
            quote_line_obj = QuoteLineItem()
            quote_line_obj.quote = quote_obj
            quote_line_obj.quantity = 1
            quote_line_obj.model = product_refrence
            prod_description = quote_requested_product_configuration.format (u=user, s=settings, p=Prod(prod))
            prod_description = prod_description.strip()
            quote_line_obj.description = prod_description
            quote_line_obj.image = image_url
            quote_line_obj.cost = product.cost
            if quote_details:
                quote_line_obj.comments = "User quote details : %s" %quote_details
            quote_line_obj.price = product.baseprice
            quote_line_obj.save()

            # Save ipaddress
            if ipaddress:
                activity_name = 'Request-a-quote'
                ip_add = IpAddress()
                ip_add.quote = quote_obj
                ip_add.ip_address = ipaddress
                ip_add.comments = "saved Request-a-quote user %s IP-Address" % user
                ip_add.activity = activity_name
                ip_add.customer = cust
                ip_add.save()

            if trace: print 'USER', user, user.is_authenticated()
            send_quote_email(req, user, notes=quote_details or "")

    return EmailForm


#### View functions

def config (request, legacy_category=None):  # redirect legacy Zope URLs to new product page
    sku = request.GET.get ('sku')

    if legacy_category:
        category = slugify (legacy_category)
    else:
        product = Product.objects.filter (sku=sku)
        if product:
            category = product [0].category.slug
        else:
            raise Http404

    return HttpResponseRedirect ('/products/%s/%s' % (category, sku))


#def products (request):  # really categories
#    categories = Categories.objects.published()
#
#    return render_to_response('products.html', dict (
#            title="eRacks Product Categories",
#            categories=categories,
#            breadcrumbs=(product_breadcrumb,),
#        ), context_instance=RequestContext(request))


def categories (request):
    categories = Categories.objects.published()

    return render_to_response('categories.html', dict (
            title="eRacks Product Categories",
            categories=categories,
            breadcrumbs=(product_breadcrumb,),
        ), context_instance=RequestContext(request))


def category (request, category):
    categories = Categories.objects.published().filter (slug=category)

    if not categories:
        categories = Categories.objects.published().filter (name__iexact=category)
        if categories:
            return HttpResponseRedirect ('/products/%s/' % categories [0].slug)

    if not categories:
        raise Http404, "Unknown Category"  # allows for redirect lookup too

    category = categories [0]

    breadcrumbs = (
        product_breadcrumb,
        category
    )

    return render_to_response('category.html', dict (
            title=category.title or category.name,
            category=category,
            breadcrumbs=breadcrumbs,
            meta_title=category.meta_title,
            meta_keywords=category.meta_keywords,
            meta_description=category.meta_description,
        ), context_instance=RequestContext(request))



def product (request, category, sku):
    products = Product.objects.filter (sku__iexact=sku)

    if products:
        product = products [0]
        if product.sku != sku:
            return HttpResponseRedirect (product.url)
        if product.category.slug != category:
            return HttpResponseRedirect (product.url)
    else:
        raise Http404, "Unknown Product"

    edit = request.GET.get ('edit', None)

    ses_helper = SessionHelper (request.session)
    if not edit:
        ses_helper.fill (product)
    else:
        assert request.session.get ('prod', None)

    post = request.POST #.copy()  # make it mutable to add sku

    if post:  # only for small subform(s) like email quote and future wishlist
        if post.get('quote', None):
            # send quote request to admin & user both, save in quotes
            #print 'POST', post
            #request.user.email
            emailform = emailForm (request, product) (post)
            email = request.POST.get ("email")

            if emailform.is_valid():
                #Do we need this? we already just validated it
                #emailform = emailForm (request, product)()
                if email:
                    sent_email = email
                else:  # if form is vaolid, then this is lways true: if request.user.is_authenticated():
                    sent_email = request.user.email

                messages.success (request, 'Your quote request has been sent to %s' % sent_email)

        elif post.get ('wishlist', None):     # Add reference to this product in user's wishlist
            raise Exception ('Implement Wishlist!')
        else:
            add_to_cart (request)
            return HttpResponseRedirect('/cart/')

    else:
        emailform = emailForm(request,product)()

    breadcrumbs = (
        product_breadcrumb,
        product.category,
        product,
    )

    photos_list = [str(t) for t in product_photos (product)]
    photos = mark_safe ('\n'.join (photos_list))

    return render_to_response ('product.html', dict (
            title=product.title or product.name,
            product=product,
            breadcrumbs=breadcrumbs,
            meta_title=product.meta_title,
            meta_keywords=product.meta_keywords,
            meta_description=product.meta_description,
            photos=photos,
            photos_list=photos_list,
            emailform=emailform,
            js_bottom=mark_safe (tags.script (config_grid_js, type='text/javascript')),
        ), context_instance=RequestContext(request))



#### Ajax views and supporting

#@is_ajax or ajax_required...
def update_grid (request):
    ses_helper = SessionHelper (request.session)
    results = ses_helper.update (request)
    return HttpResponse (json.dumps (results), content_type='application/json')


#### configgrid view with js

config_grid_js='''
function update_config (e) {
    console.log ($('.configform').serialize());
    if (e) {
        console.log ('ITEM CHANGED:');
        console.log (e.currentTarget);
        console.log ($(e.target).find ('option:selected'));
    }

    $.post ("/products/update_grid/", $('.configform').serialize(), function(json) {
        console.log (json);
        $('#config_summary .price b').html ('$' + json.price);
        $('#config_summary .summary').html ('<b>Configuration Summary:</b><br>' + json.summary);

        $.each(json.optchoices, function(key, val) {  // it's an array, so keys are 0
            console.log (key, val);
            console.log ('#' + val.optid + ' .info');
            if (val.choicename)
                $('#' + val.optid + ' .info').html (val.choicename);
            if (val.choiceblurb)
                $('#' + val.optid + ' .info').attr ('title', val.choiceblurb);
            //if (val.optprice)
            $('#' + val.optid + ' .optprice').html ('$' + val.optprice);
        });
    }).error (function(err) {
        console.log ('post error:' + err);
        window.location.reload();   // likely the back button, prod is no longer there, so reload
    });
}

$(document).ready(function() { // JJW changed this to load 1/10/13, was firing before GET completed, causing inv inx
//$(document).load(function() {  // nope, doesn't fire at all now :(
    //update_config();

    $('.configgrid select[name="choiceid"]').change (update_config);
    $('.configgrid select[name="choiceqty"]').change (update_config);
});
'''
