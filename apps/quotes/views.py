#from django.utils.encoding import smart_str, smart_unicode
import cgi
from cStringIO import StringIO

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives

from weasyprint import HTML

from utils import Breadcrumb
from quotes.models import Quote  #, QuoteLineItem
from customers.models import Customer, Address,AddressForm, BillingAddressForm, CustomerForm

company = 'eRacks'
company_short = company

## Private quotes for user, with list

quote_viewed_template = '''
{s.HOST_NAME} user accessed quote:

User: {u.username}
eMail: {u.email}

IP address: {ip}

Quote: {r.path}
'''

@login_required  # we can tie in the user later, but at least make him log in
def quote (req, num=None, pdf=False):
    user = req.user
    quote_breadcrumb = Breadcrumb ('Quotes', 'eRacks Quote List for %s' % user, '/quotes/')
    
    if 0:  # messages_test
        from django.contrib import messages
        #messages.add_message(req, messages.INFO, 'Hello world.')

        #Some shortcut methods provide a standard way to add messages with commonly used tags (which are usually represented as HTML classes for the message):

        messages.debug(req, '%s SQL statements were executed.' % 123)
        messages.info(req, '%s SQL statements were executed.' % 123)
        messages.info(req, 'Three credits remain in your account.')
        messages.success(req, 'Profile details updated.')
        messages.warning(req, 'Your account expires in three days.')
        messages.error(req, 'Document deleted.')

    if num:
        # render it directly

        try:
            q = Quote.objects.get (quote_number=num)
        except Quote.DoesNotExist:
            raise Http404

        if q:
            address1 = Address.objects.filter(customer=q.customer)
        #print address1
        shipping_addr = None
        billing_addr = None
        if address1:
            for address in address1:
                print address.type
                if address.type=="shipping":
                    shipping_addr = address
                if address.type=="billing":
                    billing_addr = address
                if address.type=="both":
                    shipping_addr = address
                    billing_addr = address

        prod = dict (
                address1      = address1,
                shipping_addr = shipping_addr,
                billing_addr  = billing_addr,
                q           = q,
                totprice    = q.totprice,
                summary     = q.summary,
                notes       = q.header_items, # terms, discounts, etc?
                #qty        = q.totqty,
                qty         = 1,
                opts        = {},
                baseprice   = q.totprice,
                weight      = q.shipping,
                sku         = 'Quote/%s' % q.quote_number,
                order_total =   q.totprice + q.shipping
            )

        if req.POST.get ('add', None):  # add quote to cart as product
            prod = dict (
                totprice    =   q.totprice,
                summary     =   q.summary,
                notes       =   q.header_items, # terms, discounts, etc?
                #qty        =   q.totqty,
                qty         =   1,
                opts        =   {},
                baseprice   =   q.totprice,
                weight      =   q.shipping,
                sku         =   'Quote/%s' % q.quote_number,
                order_total =   q.totprice + q.shipping
            )
            ses = req.session
            ses ['cart'] = ses.get ('cart', []) + [prod]
            ses ['prod'] = {}

            return HttpResponseRedirect ('/cart/')


        text = "Your email confirmation, as PDF attachment\n\n"
        html_string = render_to_string ('pdf/index.html', context=prod)
        html = HTML(string=html_string,base_url=req.build_absolute_uri())
        pdf = html.write_pdf()
        #return HttpResponse (pdf, content_type='application/pdf')

        msg = EmailMultiAlternatives ('Your %s eracks quote #%s' % (settings.HNN[0],q.quote_number),
                text,  # nope: '',  # let's try attaching the text,
                settings.ORDER_FROM_EMAIL,
                ['manikantak_nyros@yahoo.com']
            )
        msg.attach ('eRacks_Quote_#%s.pdf' % q.quote_number, pdf, "application/pdf")
        # msg.send()

        if req.POST.get ('pdf', None):  # Render PDF file & return to user
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=eRacks_Quote_#%s.pdf' % q.quote_number
            response.write(pdf)
            return response


        # Drop thru: email admin, render the quote_number

        if not user.is_staff:
            subject = "%s user accessed %s" % (settings.HOST_NAME, req.path)
            ip = req.META.get ('HTTP_X_FORWARDED_FOR', req.META.get ('HTTP_X_REAL_IP', req.META.get ('REMOTE_ADDR', 'unknown')))
            message = quote_viewed_template.format (s = settings, ip = ip, u = user, r = req)
            to = settings.CONTACT_EMAILS
            fm = 'django.admin@eracks.com'  # user.email
            send_mail (subject, message, fm, to, fail_silently = not settings.DEBUG)

        for line in q.quotelineitem_set.all():  # lame: dj templates can't do multiplcation or expressions
            line.ext = line.quantity * line.price

        return render_to_response('quote.html',
          dict (
            title="Quote: %s" % q.quote_number,
            q=q,
            breadcrumbs = (quote_breadcrumb, Breadcrumb ('Quote %s' % q.quote_number, 'Quote %s' % q.quote_number, '/quotes/%s' % q.quote_number))
          ),
          context_instance=RequestContext(req))
    else:
        # render the list
        if user.is_staff:
            qs = Quote.objects.filter (approved_by=user)
        else:
            qs = Quote.objects.filter (customer__user=user)

        return render_to_response('entries.html',
            dict (
                entries = qs,
                title = 'Quote list for %s' % user,
                breadcrumbs = (quote_breadcrumb,),
            ),
            context_instance=RequestContext(req))
