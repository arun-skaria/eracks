"""
These are the tests for the quotes app.
"""

import time

from django.conf import settings
from django.test import TestCase, Client
from django.test.utils import override_settings

from quotes.models import *
from products.views import send_quote_email

from utils.tests import find_first, drivers_present, test_drivers, MyLiveTestCase


breakpoint = 0
#trace = 0


class FixturesTest(TestCase):
    fixtures = ['quotes-55143.yaml']  # 'customers.yaml', 'users.yaml',

    def test_customers_fixtures(self):
        quote1 = Quote.objects.get(pk=55143)
        self.assertTrue(quote1)


class QuoteTest(TestCase):
    def setUp(self):
        user2 = User.objects.create(username="testuser2",email="testuser2@yahoo.com",password="testuser2")

        customer2 = Customer.objects.get (user=user2)

        quote1 = Quote.objects.create (
          customer=customer2,
          quote_number='022222-LAPI',
          approved_by=user2,
          valid_for=10,
          purchase_order='2222-P-00-260563',
          customer_reference='Laptop note, 48 cores',
          terms='ccard',
          shipping=222,
          target=22222
        )

        quotelineitem1 = QuoteLineItem.objects.create (
            quote=quote1,
            model='lapi222',
            quantity=22,
            description='descriptiondescription',
            cost=2222.22,
            price=2222
          )

    def test_is_template(self):
        quote1 = Quote.objects.get(quote_number='022222-LAPI')
        self.assertFalse(quote1.is_template())

    def test_totprice(self):
        quote1 = Quote.objects.get(quote_number='022222-LAPI')
        for q in quote1.quotelineitem_set.all():
            total_price = q.price*q.quantity
        self.assertEqual(quote1.totprice, total_price)

    def test_totqty(self):
        quote1 = Quote.objects.get(quote_number='022222-LAPI')
        self.assertEqual(quote1.totqty, 22)

    def test_summary(self):
        quote1 = Quote.objects.get(quote_number='022222-LAPI')
        self.assertTrue(quote1.summary)

    def test_header_items(self):
        quote1 = Quote.objects.get(quote_number='022222-LAPI')
        self.assertTrue(quote1.header_items)



if drivers_present():      # In-browser tests - only performed if Firefox and/or Chrome are present
    class LiveQuotesTests (MyLiveTestCase):
        fixtures = ['products-2.yaml']  # 'quickpages.yaml','users.yaml','bloglets.yaml', 'products_all.yaml', 'home.yaml']
        #fixtures = ['user-data.json']
        csrf_client = Client(enforce_csrf_checks=True)

        def setUp(self):
            user1 = User.objects.create_user(username="test1_eracks@yopmail.com",email="test1_eracks@yopmail.com",password="testuser1")
            my_admin = User.objects.create_superuser('joe', 'myemail@test.com', 'myuser')

        @override_settings(DEBUG=True)
        @test_drivers()
        def test_login_without_name_email_quotedetails(self):
            "Get quote with user logged in without filling in email field"
    
            self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
            time.sleep(2)
        
            ## Select the visible ones, not the modal(hidden) one - fill in user & pw, submit
            username_input = find_first (self.selenium, '#content_row input#id_identification', '#content input#id_identification')
            username_input.send_keys('test1_eracks@yopmail.com')
            password_input = find_first (self.selenium, '#content_row input#id_password', '#content input#id_password')
            password_input.send_keys('testuser1')
            find_first(self.selenium, '#content_row input[type=submit][value=Signin]', '#content input[type=submit][value=Signin]').click()
            time.sleep(2)
        
            ## Grab screens
            self.screengrabs ('test_login.png')
            logedin = self.selenium.page_source
            self.assertIn ("You have been signed in", logedin)                     

            ## Load product page
            self.selenium.get('%s%s' % (self.live_server_url, '/products/firewall-servers/DMZ/'))
            time.sleep (2)
                        
            ## Get quote
            click_getquote = self.selenium.find_element_by_id('get_quote').click()
            source = self.selenium.page_source
            sentemail = self.selenium.find_element_by_css_selector('#content div.alert.alert-success.alert-dismissible').text

            ## Grab screens
            self.screengrabs ('quote_test_logged_in_without_email.png')
            self.assertIn ("Your quote request has been sent to test1_eracks@yopmail.com", sentemail)

        @override_settings(DEBUG=True)
        @test_drivers()
        def test_login_with_name_email_quotedetails(self):
            "Get quote with user logged in with filled-in email field"

            before_get_quote = User.objects.all().count()

            self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
            time.sleep(2)
        
            ## Select the visible ones, not the modal(hidden) one - fill in user & pw, submit
            username_input = find_first (self.selenium, '#content_row input#id_identification', '#content input#id_identification')
            username_input.send_keys('test1_eracks@yopmail.com')
            password_input = find_first (self.selenium, '#content_row input#id_password', '#content input#id_password')
            password_input.send_keys('testuser1')
            find_first (self.selenium, '#content_row input[type=submit][value=Signin]', '#content input[type=submit][value=Signin]').click()
            time.sleep(2)
        
            ## Grab screens
            self.screengrabs ('test_login.png')
            self.assertIn ("You have been signed in", self.selenium.page_source) 

            ## Load product page
            self.selenium.get('%s%s' % (self.live_server_url, '/products/firewall-servers/DMZ/'))
            time.sleep (2)

            ## Fill in email and get quote
            email = self.selenium.find_element_by_css_selector('div#config.pull-left form.configform #id_email')
            email.send_keys("test_withemail_eracks@yopmail.com")
            override_email = User.objects.filter(email ="test1_eracks@yopmail.com").update(email="test_withemail_eracks@yopmail.com")
            click_getquote = self.selenium.find_element_by_id('get_quote').click()
            time.sleep (2)

            ## Get count for comparison, check email msg
            after_get_quote = User.objects.all().count()
            sentemail = self.selenium.find_element_by_css_selector('#content div.alert.alert-success.alert-dismissible').text

            ## Grab screens
            self.screengrabs ('quote_test_loggedin_with_email.png')
            self.assertIn("Your quote request has been sent to test_withemail_eracks@yopmail.com", sentemail)
            self.assertEqual(before_get_quote, after_get_quote)

        @test_drivers()
        def test_logout_with_username_email_quotedetails(self):
            "Get quote with user not logged in and filled-in name email quotedetails field"

            before_get_quote = User.objects.all().count()

            ## Load login page
            self.selenium.get('%s%s' % (self.live_server_url, '/products/firewall-servers/DMZ/'))
            username = self.selenium.find_element_by_css_selector('form.configform #id_name')
            username.send_keys("testemail")
            email = self.selenium.find_element_by_css_selector('form.configform #id_email')
            email.send_keys("testemail_eracks@yopmail.com")
            quotedetails = self.selenium.find_element_by_css_selector('form.configform #notes')
            quotedetails.send_keys("test eracks quote details inforamtion like timeframe special request etc..")            
            create_user = User.objects.create(username="testemail_eracks@yopmail.com",email ="testemail_eracks@yopmail.com")
            time.sleep(5)
            click_getquote = self.selenium.find_element_by_id('get_quote').click()
            time.sleep(2)

            ## Get count for comparison, send email
            after_get_quote = User.objects.all().count()

            ## grab screens
            self.screengrabs ('quote_test_not_logged_in_with_username_email_quotedetails.png')
            self.assertEqual(after_get_quote, before_get_quote+1)

        @test_drivers()
        def test_logout_without_username_email_quotedetails(self):
            "Get quote with user not logged in and without filling in username field  email field and quotedetail field"

            self.selenium.get('%s%s' % (self.live_server_url, '/products/firewall-servers/DMZ/'))
            click_getquote = self.selenium.find_element_by_id('get_quote').click()
            time.sleep (2)
            error = self.selenium.find_element_by_css_selector('div#config.pull-left form.configform div.col-md-6 ul.errorlist li').text

            ## Grab screens
            self.screengrabs ('quote_test_not_loggedin_without_username_email_quotedetails.png')
            self.assertIn ("You must either be logged in, or enter your name and email address and quote details to receive your quote.", error)

