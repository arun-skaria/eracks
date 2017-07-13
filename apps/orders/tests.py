"""
This is the tests file for the orders module.

Notable is the test_order test, which will run when you do:

./manage.py test orders.tests.LiveOrdersTest

or test all.

If you have trouble debugging, you may set 'breakpoint' to 1 near the top, which will break into an IPython shell at
the point in the code where it is referenced - see the code for usage.
"""

import time
from datetime import datetime

from django.test import TestCase
from django.test import Client
from django.conf import settings

from django.core import mail
from orders.models import *
from customers.models import *
from products.models import *
from email_extras.utils import send_mail
from utils.tests import find_first, drivers_present, test_drivers, MyLiveTestCase
import os
import gnupg
from django.test.utils import override_settings



breakpoint = 0
trace = 0


if drivers_present():
    class LiveOrdersTest (MyLiveTestCase):
        fixtures = ['catax.yaml', 'products-all.yaml', 'quickpages-all.yaml']
        csrf_client = Client (enforce_csrf_checks=True)

        def setUp(self):
            if trace: print 'STARTING ORDERS SELENIUM TESTS'
            user1 = User.objects.create_user (username="test1_eracks@eracks.com", email="test1_eracks@eracks.com", password="testuser1")

        @test_drivers()
        def test_order(self):
            # import pdb;pdb.set_trace()
            from selenium.webdriver.support.select import Select

            p = Product.objects.get (sku = 'DMZ')
            shipping_weight = p.weight
            if trace: print 'SHIPPING WEIGHT:', shipping_weight
            self.selenium.get ('%s%s' % (self.live_server_url, '/products/firewall-servers/DMZ/'))
            time.sleep(2)

            ## Click an 'Add to cart' button, update quantity
            find_first (self.selenium,'input#add_to_cart').click()
            time.sleep(10)
            update_qty = self.selenium.find_element_by_name ('updqty')
            time.sleep(2)
            update_qty.send_keys ('2')
            time.sleep(2)
            self.selenium.find_element_by_name ('update').click()
            time.sleep (2)

            ## Now move to checkout page
            checkout = find_first (self.selenium, '#next a[href="/checkout/"]','#order-detail-content a[href="/checkout/"]')
            self.selenium.execute_script ("return arguments[0].scrollIntoView();", checkout)
            checkout.click()
            time.sleep(2)
            form_heading = self.find_first ('#content form fieldset legend')
            self.assertIn ('Signin', form_heading.text)

            ## User Login form
            username_input = find_first (self.selenium, '#content_row input#id_identification','div#content input#id_identification')
            username_input.send_keys ('test1_eracks@eracks.com')
            password_input = find_first (self.selenium, '#content_row input#id_password','div#content input#id_password')
            password_input.send_keys('testuser1')
            find_first (self.selenium, '#content_row form input[type=submit][value=Signin]','div#content form input[type=submit][value=Signin]').click()
            time.sleep(2)
            h1 = self.find_first ('#content h1')
            self.assertIn ('Checkout', h1.text)

            ## User Info Form - should be pre-filled-in, no need
            ## Customer Info form
            organization = self.selenium.find_element_by_css_selector ('table#CustomerForm input#id_organization')
            organization.send_keys ('test')
            title = self.selenium.find_element_by_css_selector ('table#CustomerForm input#id_title')
            title.send_keys ('test')
            department = self.selenium.find_element_by_css_selector ('table#CustomerForm input#id_department')
            department.send_keys ('test')
            email_id = self.selenium.find_element_by_css_selector ('table#CustomerForm input#id_email')
            email_id.send_keys ('test1_eracks@yopmail.com')
            phone = self.selenium.find_element_by_css_selector ('table#CustomerForm input#id_phone')
            phone.send_keys ('+919999999999')

            ## Order Info Form
            referral_type = Select (self.selenium.find_element_by_css_selector ('table#OrderForm select#id_referral_type'))
            referral_type.select_by_visible_text ("Google search")
            sales_tax = Select (self.selenium.find_element_by_css_selector ('table#OrderForm select#id_california_tax'))
            sales_tax.select_by_visible_text ('Los Angeles')
            agree_to_terms = self.selenium.find_element_by_css_selector ('table#OrderForm input#id_agree_to_terms')
            agree_to_terms.click()  # send_keys(' ') nfg

            if breakpoint:
                from IPython import embed
                embed()

            ## Shipping Address Form
            address1 = self.selenium.find_element_by_css_selector ('table#AddressForm input#id_shipping-address1')
            address1.send_keys ('test street, 5-4-20')
            city = self.selenium.find_element_by_css_selector ('table#AddressForm input#id_shipping-city')
            city.send_keys ('Los Angeles')
            state = Select (self.selenium.find_element_by_css_selector('table#AddressForm select#id_shipping-state'))
            state.select_by_visible_text ('CA (California)')
            zip_code = self.selenium.find_element_by_css_selector ('table#AddressForm input#id_shipping-zip')
            zip_code.send_keys ('90011')

            ## Billing Address Form (use selector table#BillingAddressForm input#id_billing_name, etc)
            # if blank same as shipping, but could still test here..

            ## Payment Info Form
            payment_method1 = Select (self.selenium.find_element_by_css_selector ("table#PaymentForm select#id_payment_method"))
            payment_method1.select_by_visible_text ("Purchase Order")
            expiry_date1 = Select (self.selenium.find_element_by_css_selector ('table#PaymentForm select#id_expiry_date_1'))
            expiry_date1.select_by_visible_text ('2017')
            time.sleep (2)

            ## Click confirm
            confirm_button = find_first (self.selenium, 'input[name=update][value=Update]','form#checkoutform div#content_row a[href="/checkout/confirm/"]')
            if trace: print confirm_button.text
            confirm_button.click()
            time.sleep (2)
            h1 = self.find_first ('#content h1')
            self.assertIn ('Checkout - Review/Confirm Your Order', h1.text)

            actual_shipping = self.selenium.execute_script ('''return $("#final_cart table td:contains(Shipping & Handling)+td").get(0)''')

            if breakpoint:
                from IPython import embed
                embed()

            if trace: print 'actual_shipping', type(actual_shipping), actual_shipping.text
            actual_shipping_price  = float(actual_shipping.text.strip('$'))
            expected_shipping_price = shipping_weight*2

            ## Place the order!
            find_first(self.selenium, '#content_row input[name=order][value="Place Order"]','form#confirmform a[href="/checkout/confirm/"]').click()
            time.sleep (2)

            self.screengrabs ('test_order.png')
            self.assertEqual (expected_shipping_price, actual_shipping_price)


class FixturesTest(TestCase):
    # Maybe could do: nested orders dump includes user, userena, customer - JJW no need for: 'users.yaml', 'customers.yaml', 'catax.yaml',
    fixtures = ['orders-one.yaml'] #, 'users.yaml', 'customers.yaml',]

    #def _fixture_setup (self):
    #    print 'FIXTURES SETUP'
    #    print 'CUSTOMERS', Customer.objects.all()

    #@classmethod
    #def setUpClass(cls):
    #    print 'SETUP CLASS'
    #    print 'CUSTOMERS B', Customer.objects.all(), Customer.objects.all().values()
    #    super(FixturesTest, cls).setUpClass()
    #    print 'CUSTOMERS A', Customer.objects.all()

    #def setUp(self):
    #    print 'SETUP'
    #    print 'CUSTOMERS', Customer.objects.all()

    def test_orders_fixtures(self):
        order1 = Order.objects.get(pk=57138)
        self.assertTrue (order1)


class ViewsTests(TestCase):
    fixtures = ['catax.yaml', 'products-all.yaml', 'quickpages.yaml', 'orders-one.yaml']  #, 'customers.yaml', 'users.yaml',]

    def test_cart(self):
        client = Client()
        response = client.get("/cart/")
        if trace: print 'CART', response.content
        self.assertEqual(response.status_code, 200)
        # need to set the session with products for post request

    def test_cart_post(self):
        client = Client()
        products = Product.objects.all()
        response = client.post("/cart/", {'prod': products[0]})
        self.assertIn('cart is empty', response.content)
        #without product checkout is redirecting to cart page

    def test_checkout(self):
        client = Client()
        response = client.get("/checkout/", follow=True)
        self.assertIn ('Your Cart', response.content)


class ImportedOrderTests(TestCase):
    def setUp(self):
        importorder1 = ImportedOrder.objects.create (
          title='test@test.com',
          email='test@test.com',
          shiptype='US',
          shipname='test',
          shiporg='test1',
          shipaddr1='26246 Twelve Trees Lane NW',
          shipcity='los angeles',
          shipmethod='Ground',
          shipcost='0',
          shippay='shipincl',
          billsame='on',
          iagree='on',
          reftyp='repeat',
          paymeth='byccard',
          orderstatus='open',
          ordernum='54364',
        )

    def test_name(self):
        importedorder1 = ImportedOrder.objects.get(title='test@test.com')
        shipname1 = importedorder1.shipname
        name1 = importedorder1.name()
        self.assertEqual(shipname1, name1)

    def test_org(self):
        importedorder1 = ImportedOrder.objects.get(title='test@test.com')
        shiporg1 = importedorder1.shiporg
        org1 = importedorder1.org()
        self.assertEqual(shiporg1, org1)

    def test_name_org(self):
        importedorder1 = ImportedOrder.objects.get(title='test@test.com')
        name_org1 = importedorder1.name_org()
        self.assertTrue(name_org1)


class OrderPaymentTest(TestCase):
    def setUp(self):
        ex_date = datetime (2015, 12, 31, 18, 23, 29, 227)
        user2 = User.objects.create (username="testuser2", email="testuser2@yahoo.com", password="testuser2")
        customer2 = Customer.objects.get (user=user2)

        address2 = Address.objects.create (
          customer=customer2,
          address2='street',
          city='texas',
          state='CA',
          zip='556655',
          country='US',
          phone='123456',
          email='testuser2@yahoo.com',
          type='shipping'
        )

        order1 = Order.objects.create (
          customer=customer2,
          shipping=40.00,
          shipping_method='ground',
          preferred_shipper='Any',
          referral_type='google',
          ship_to_address=address2,
          bill_to_address=address2,
          status='website',
          source='website'
        )

        orderpayment1 = OrderPayment.objects.create (
          order=order1,
          payment_method='byccard',
          expiry_date=ex_date,
          user=user2
        )

    def test_expiry_mmyy(self):
        user2 = User.objects.get(email='testuser2@yahoo.com')
        customer2 = Customer.objects.get(user=user2)
        order1 = Order.objects.get(customer=customer2)
        orderpayment1 = OrderPayment.objects.get(order=order1)
        if trace: print 'ORDERPAYMENT', orderpayment1, 'EXPIRES', orderpayment1.expiry_mmyy()
        self.assertEqual (orderpayment1.expiry_mmyy(), '1215')
  


@override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
class EmailTest(TestCase):
    
    def test_gpg_key_encryption_mail(self):
        from email_extras.models import Address
        GNUPG_HOME = getattr(settings, "EMAIL_EXTRAS_GNUPG_HOME", None)
        USE_GNUPG = getattr(settings, "EMAIL_EXTRAS_USE_GNUPG", GNUPG_HOME is not None)        
        gpg = gnupg.GPG(gnupghome=GNUPG_HOME) #'/home/sysadmin/gpghome'
        input_data = gpg.gen_key_input(
            name_email='joe@eracks.com',
            passphrase='my passphrase')
        key = gpg.gen_key(input_data)
        address = Address.objects.create(address="joe@eracks.com")
        subject = "test subject for email encryption and send"
        body_text = "test body text for email encryption and send"
        addr_from = "testorders@eracks.com"
        addr_to = ["joe@eracks.com","testemail_eracks@yopmail.com"]
        mail_sent_success = send_mail(subject,body_text,addr_from,addr_to) 
        self.assertEquals(mail_sent_success,None) 
        print 'successfully send email'



