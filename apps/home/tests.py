import unittest
import time
#import urllib
import urlparse
import os.path

from django.conf import settings
from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User, Group
from home.models import *
from home.views import testing_social_auth_by_access_token
from django.contrib.sessions.middleware import SessionMiddleware
from utils.tests import find_first, drivers_present, test_drivers, MyLiveTestCase

#from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from htmlvalidator.client import ValidatingClient
from xml.dom import minidom

#for social login testcases
#import json
#from social.exceptions import AuthUnknownError, AuthCanceled
#from social.tests.backends.oauth import OAuth2Test





trace = 0
breakpoint = 0

if drivers_present():      # In-browser tests - only performed if Firefox and/or Chrome are present
    #@unittest.skip ("These are hanging - both in wercker and on mintstudio - let's get the test suite working first")
    class LiveHomePageTests (MyLiveTestCase):
        fixtures = ['products-all.yaml', 'customers-54730.yaml', 'home-test.yaml',]  # 'quickpages.yaml','users.yaml','bloglets.yaml', 'user-data.json']

        def setUp(self):
            ## Set up user for login tests
            user1 = User.objects.create_user (username="test1_eracks@yopmail.com", email="test1_eracks@yopmail.com", password="testuser1")
            my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'myuser')

            ## Set up search index for test_search
            from django.core.management import call_command
            call_command ('rebuild_index', verbosity = 1, interactive = False)


        @test_drivers()
        def test_search(self):
            self.selenium.get ('%s%s' % (self.live_server_url, '/'))
            time.sleep(2)

            ## Select the visible ones, not the modal(hidden) one - fill in user & pw, submit
            search_input = self.find_first ('.search-box input', 'form#search .input_text', 'form#search_form input')
            search_input.send_keys ('dmz')
            self.find_first ('.search-box button', 'form#search .button', 'form#search_form button').click()
            time.sleep(2)

            ## Grab screens
            self.screengrabs ('test_search.png')
            self.assertIn ("DeMilitarized Zones", self.selenium.page_source)


        @override_settings (DEBUG=True)
        @test_drivers()
        def test_login(self):
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
              

        @override_settings (DEBUG=True)
        @test_drivers()
        def test_signindialog(self):
            if breakpoint:
              from IPython import embed
              embed()  # breaks into an ipython shell here!

            self.selenium.get('%s%s' % (self.live_server_url, '/'))
            time.sleep(2)

            ## Make popup visible by clicking Login
            find_first (self.selenium, "#header_right ul li:first-child a", 'a#show-login-dialog', '#show-login-dialog .glyphicon-log-in').click()
            time.sleep(2)

            ## Enter username & email
            username_input = self.selenium.find_element_by_id('id_identification')
            username_input.send_keys('test1_eracks@yopmail.com')
            password_input = self.selenium.find_element_by_css_selector('input#id_password')
            password_input.send_keys('testuser1')

            ## Submit the form, grab screens
            find_first (self.selenium, '#signinTab form input[value=Signin]', '#signin form input[value=Signin]').click()
            time.sleep(2)
            self.screengrabs ('test_signindialog.png')
            self.assertIn("You have been signed in", self.selenium.page_source)

        @override_settings(DEBUG=True)
        @test_drivers()
        def test_signupdialog(self):
            self.selenium.get('%s%s' % (self.live_server_url, '/'))
            time.sleep(2)

            ## Make popup visible by clicking Login
            find_first (self.selenium, "#header_right ul li:first-child a", "a#show-login-dialog", '#show-login-dialog .glyphicon-log-in',).click()
            time.sleep(2)

            if breakpoint:
              from IPython import embed
              embed()  # breaks into an ipython shell here!

            ## click Signup tab, enter username & email
            self.selenium.find_element_by_css_selector('#signin_signup_modal a[href="#signup"]').click()
            username = self.selenium.find_element_by_id('id_username')
            if self.selenium.name=='chrome':
                username.send_keys('test114c_eracks')
            if self.selenium.name=='firefox':
                username.send_keys('test114f_eracks')
            email = self.selenium.find_element_by_id ('id_email')
            if self.selenium.name=='chrome':
                email.send_keys('test114c_eracks@yopmail.com')
            if self.selenium.name=='firefox':
                email.send_keys('test114f_eracks@yopmail.com')
            time.sleep(2)

            ## Submit the form
            find_first (self.selenium, '#signupTab form input[value=Signup]', '#signup form input[value=Signup]').click()
            time.sleep(2)

            ## Save screenshots
            self.screengrabs ('test_signupdialog.png')
            self.assertIn ('Thank', self.selenium.page_source)

        @test_drivers()
        def test_signup_username(self):
            self.selenium.get('%s%s' % (self.live_server_url, '/accounts/signup/'))
            time.sleep(2)

            ## Fill in username
            username = find_first (self.selenium, '#content_row input#id_username','#content input#id_username')
            if self.selenium.name=='chrome':
                username.send_keys('test113c_eracks')
            if self.selenium.name=='firefox':
                username.send_keys('test113f_eracks')

            ## Fill in email
            email = find_first (self.selenium, '#content_row input#id_email', '#content input#id_email')
            if self.selenium.name=='chrome':
                email.send_keys('test113c_eracks@yopmail.com')
            if self.selenium.name=='firefox':
                email.send_keys('test113f_eracks@yopmail.com')

            ## Submit form, save screen grabs
            find_first (self.selenium, '#content_row input[type=submit][value=Signup]', '#content input[type=submit][value=Signup]').click()
            time.sleep(2)
            self.screengrabs ('test_signup_username.png')
            self.assertIn('Thank', self.selenium.page_source)

        @test_drivers()
        def test_signup_email(self):
            self.selenium.get('%s%s' % (self.live_server_url, '/accounts/signup/'))
            time.sleep(2)

            ## Fill in username
            username = find_first (self.selenium, '#content_row input#id_username', '#content input#id_username')
            if self.selenium.name=='chrome':
                username.send_keys('test112c_eracks@yopmail.com')
            if self.selenium.name=='firefox':
                username.send_keys('test112f_eracks@yopmail.com')

            ## Fill in email
            email = find_first (self.selenium, '#content_row input#id_email', '#content input#id_email')
            if self.selenium.name=='chrome':
                email.send_keys('test112c_eracks@yopmail.com')
            if self.selenium.name=='firefox':
                email.send_keys('test112f_eracks@yopmail.com')

            ## Submit form, grab screens
            find_first (self.selenium, '#content_row input[type=submit][value=Signup]', '#content input[type=submit][value=Signup]').click()
            time.sleep(2)
            self.screengrabs ('test_signup_email.png')
            self.assertIn('Thank', self.selenium.page_source)
            
            
        @test_drivers()
        def test_signup_fail_username(self):
            self.selenium.get('%s%s' % (self.live_server_url, '/accounts/signup/'))
            time.sleep(2)

            ## Fill in username
            username = find_first (self.selenium, '#content_row input#id_username', '#content input#id_username')
            if self.selenium.name=='chrome':
                username.send_keys('test112c+eracks')
            if self.selenium.name=='firefox':
                username.send_keys('test112f+eracks')

            ## Fill in email
            email = find_first (self.selenium, '#content_row input#id_email', '#content input#id_email')
            if self.selenium.name=='chrome':
                email.send_keys('test112c+eracks@yopmail.com')
            if self.selenium.name=='firefox':
                email.send_keys('test112f+eracks@yopmail.com')

            ## Submit form, grab screens
            find_first (self.selenium, '#content_row input[type=submit][value=Signup]', '#content input[type=submit][value=Signup]').click()
            time.sleep(2)
            self.screengrabs ('test_signup_fail_email.png')
            self.assertIn('not allowed', self.selenium.page_source)        
            
        @test_drivers()
        def test_contact(self):
            self.selenium.get('%s%s' % (self.live_server_url, '/contact/'))
            time.sleep(2)

            name = self.selenium.find_element_by_id("id_name")
            name.clear()
            name.send_keys("name1")

            email = find_first (self.selenium, '#content_row input#id_email', '#content input#id_email')
            email.clear()
            email.send_keys("testmailname1@yopmail.com")

            desc = self.selenium.find_element_by_id("id_description")
            desc.clear()
            desc.send_keys("sample description")

            body = self.selenium.find_element_by_id("id_body")
            body.clear()
            body.send_keys("sample body")

            # self.selenium.find_element_by_id("contact").click()

            submit = self.selenium.find_element_by_id("contact")
            submit.send_keys(Keys.RETURN)
            time.sleep(2)

            self.screengrabs ('test_contact.png')
            self.assertIn("Thank you", self.selenium.page_source)

        @test_drivers()
        def test_contact_long_email(self):
            self.selenium.get('%s%s' % (self.live_server_url, '/contact/'))
            time.sleep(2)

            name = self.selenium.find_element_by_id("id_name")
            name.clear()
            name.send_keys("lengthen email")

            email = find_first (self.selenium, '#content_row input#id_email', '#content input#id_email')
            email.clear()
            email.send_keys("lengthentestindevwithverylargeemailid@yopmail.com")

            desc = self.selenium.find_element_by_id("id_description")
            desc.clear()
            desc.send_keys("lengthen test with very large email")

            body = self.selenium.find_element_by_id("id_body")
            body.clear()
            body.send_keys("lengthen test with very large email")

            submit = self.selenium.find_element_by_id("contact")
            time.sleep(2)
            submit.send_keys(Keys.RETURN)
            time.sleep(2)

            self.screengrabs ('test_contact_long_email.png')
            self.assertIn("Thank you", self.selenium.page_source)

        @test_drivers()
        def test_admin_login(self):
            self.selenium.get ('%s%s' % (self.live_server_url, '/admin/login/'))
            time.sleep(2)

            username_input = self.selenium.find_element_by_css_selector ('input#id_username')
            username_input.send_keys('myuser')
            password_input = self.selenium.find_element_by_css_selector ('input#id_password')
            password_input.send_keys('myuser')
            self.selenium.find_element_by_css_selector ('input.grp-button.grp-default').click()
            time.sleep(2)

            self.screengrabs ('test_admin_login.png')
            self.assertIn("Authentication and Authorization", self.selenium.page_source)

        @test_drivers()
        def test_admin_featuredimage(self):
            self.selenium.get ('%s%s' % (self.live_server_url, '/admin/home/featuredimage/'))
            time.sleep(2)

            username_input = self.selenium.find_element_by_css_selector ('input#id_username')
            username_input.send_keys ('myuser')
            password_input = self.selenium.find_element_by_css_selector ('input#id_password')
            password_input.send_keys ('myuser')
            self.selenium.find_element_by_css_selector ('input.grp-button.grp-default').click()

            time.sleep(2)
            self.screengrabs ('test_admin_featuredimage.png')
            self.assertIn("Featured images", self.selenium.page_source)
            
          
''' Removing these three - can't get them to work in Wercker - even StaticLiveServerTestCase hangs indefinittely

Django testing is brittle and somehwat broken - grrrr.  JJW

        @override_settings (DEBUG=True)
        @test_drivers()
        def test_robots (self):
            """
            Tests whether robots.txt file is serving OK
            """
            response = self.selenium.get ("/robots.txt")
            self.assertEqual (response.status_code, 200)

        @override_settings (DEBUG=True)
        @test_drivers()
        def test_humans (self):
            """
            Tests whether humans.txt file is serving OK
            """
            response = self.selenium.get ("/humans.txt")
            self.assertEqual (response.status_code, 200)

        @override_settings (DEBUG=True)
        @test_drivers()
        def test_favicon (self):
            """
            Tests whether favicon.ico file is serving OK
            """
            response = self.selenium.get ("/favicon.ico")
            self.assertEqual (response.status_code, 200)
'''

## Unit tests

class CheckFilesTest (TestCase):  # see also the three matching live tests above - these can't go in unit tests, as they are static files
    def test_robots_present (self):
        """
        Tests whether robots file exists or not
        """
        self.assertTrue(os.path.exists('static/robots.txt'))

    def test_humans_present (self):
        """
        Tests whether humans file exists or not
        """
        self.assertTrue(os.path.exists('static/humans.txt'))

    def test_favicon_present (self):
        """
        Tests whether favicon.ico file exists or not
        """
        self.assertTrue(os.path.exists('static/humans.txt'))


class ViewsTests(TestCase):
    fixtures = ['quickpages.yaml']

    def setUp(self):
        user1 = User.objects.create_user (username="testmailname1", email="testmailname1@yopmail.com", password="testuser1")

    def test_contact(self):
        response = self.client.get ("/contact/")
        self.assertEqual (response.status_code, 200)

    def test_contact_post(self):
        client = Client()
        response = client.post(
            "/contact/", {'name': 'test', 'email': 'test@yopmail.com', 'topic': 'Network design services', 'description': 'test', 'body': 'test'})
        self.assertIn ("Thank you", response.content)

    def test_user_signup(self):
        response = self.client.get("/accounts/signup/")
        self.assertEqual (response.status_code, 200)

    def test_user_signup_post(self):
        client = Client()
        response = client.post ("/accounts/signup/", {'username': 'sometestuser', 'email': 'sometestuser@yopmail.com'})
        self.assertIn ("Thank you", response.content)

    def test_user_login(self):
        client = Client()
        response = client.post ("/accounts/login/", {'identification': 'testmailname1', 'password': 'testuser1'}, follow=True)
        self.assertIn ("You have been signed in", response.content)
        # self.assertEqual(response.status_code, 200)


class FixturesTest(TestCase):
    fixtures = ['home.yaml', 'products-all.yaml']

    def test_home_fixtures(self):
        fimage1 = FeaturedImage.objects.get(pk=56721)  # 53684)
        all_f_imgs = FeaturedImage.objects.all()
        self.assertTrue(fimage1)


class FeaturedImageTest(TestCase):
    def setUp(self):
        FeaturedImage.objects.create (
            image='images/slideshow/NAS72_frontpage.jpg', link='/testimage/',
            title='testimage',
            caption='testimage',
          )

    def test_as_img(self):
        featuredimage1 = FeaturedImage.objects.get(title='testimage')
        if trace: print featuredimage1.as_img()
        self.assertTrue(featuredimage1.as_img())

    def test_as_caption(self):
        featuredimage1 = FeaturedImage.objects.get(title='testimage')
        if trace: print featuredimage1.as_caption()
        self.assertTrue(featuredimage1.as_caption())

    def test_as_content(self):
        featuredimage1 = FeaturedImage.objects.get(title='testimage')
        if trace: print featuredimage1.as_content()
        self.assertTrue(featuredimage1.as_content())


@unittest.skip ("These are in need of work - let's get the test suite working first - then use the live fixture dump here, or a use mgmt command for this")
class HtmlValidation(TestCase):
    fixtures = ['products-all.yaml', 'customers-54730.yaml', 'quickpages.yaml', 'home-all.yaml']

    def setUp(self):
        self.client = ValidatingClient()

    def test_main_page(self):
        response = self.client.get("https://eracks.com/")
        self.assertEqual(response.status_code, 200)

    def test_services_page(self):
        response = self.client.get("https://eracks.com/services/")
        self.assertEqual(response.status_code, 200)

    def test_contact_page(self):
        response = self.client.get("https://eracks.com/contact/")
        self.assertEqual(response.status_code, 200)

    def test_customers_page(self):
        response = self.client.get("https://eracks.com/customers/")
        self.assertEqual(response.status_code, 200)

    def test_cart_page(self):
        response = self.client.get("https://eracks.com/cart/")
        self.assertEqual(response.status_code, 200)

    def test_showroom_page(self):
        response = self.client.get("https://eracks.com/showroom/")
        self.assertEqual(response.status_code, 200)

    def test_partners_page(self):
        response = self.client.get("https://eracks.com/partners/")
        self.assertEqual(response.status_code, 200)

    def test_press_page(self):
        response = self.client.get("https://eracks.com/press/")
        self.assertEqual(response.status_code, 200)

    def test_corporate_page(self):
       response = self.client.get("https://eracks.com/corporate/")
       self.assertEqual(response.status_code, 200)

    #def test_product_premium(self):
    #    response = self.client.get("https://eracks.com/products/general-purpose/PREMIUM/")
    #    self.assertEqual(response.status_code, 200)

    def test_product_dmz(self):
        response = self.client.get("https://eracks.com/products/firewall-servers/DMZ/")
        self.assertEqual(response.status_code, 200)


# SSL issue?:
# @unittest.skip("This is getting: a 302 instead of 200 - SSL issue?")
class AdminLinksTest(TestCase):
    def setUp(self):
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'myuser')
        self.client.login(username="myuser",password="myuser")

    def test_admin(self):
        """
        Tests wether can we login to admin panel or not
        """
        response = self.client.get("/admin/")
        self.assertIn("Authentication and Authorization",response.content)
    def test_admin_user(self):
        """
        Tests admin/auth/user url in admin panel
        """
        response = self.client.get("/admin/auth/user/")
        self.assertIn("Users",response.content)
    def test_admin_group(self):
        """
        Tests admin/auth/group url in admin panel
        """
        response = self.client.get("/admin/auth/group/")
        self.assertIn("Groups",response.content)
    def test_admin_redirects(self):
        """
        Tests admin/redirects url in admin panel
        """
        response = self.client.get("/admin/redirects/")
        self.assertIn("Redirects",response.content)
    def test_admin_sites(self):
        """
        Tests admin/sites/site/ url in admin panel
        """
        response = self.client.get("/admin/sites/site/")
        self.assertIn("Sites",response.content)
    def test_admin_featuredimage(self):
        """
        Tests admin/home/featuredimage url in admin panel
        """
        response = self.client.get("/admin/home/featuredimage/")
        self.assertIn("Featured images",response.content)
    def test_admin_category(self):
        """
        Tests admin/bloglets/category/ url in admin panel
        """
        response = self.client.get("/admin/bloglets/category/")
        self.assertIn("Categories",response.content)
    def test_admin_post(self):
        """
        Tests admin/bloglets/post/ url in admin panel
        """
        response = self.client.get("/admin/bloglets/post/")
        self.assertIn("Posts",response.content)
    def test_admin_quickpage(self):
        """
        Tests admin/quickpages/quickpage/ url in admin panel
        """
        response = self.client.get("/admin/quickpages/quickpage/")
        self.assertIn("Quick pages",response.content)
    def test_admin_quicksnippet(self):
        """
        Tests admin/quickpages/quicksnippet/ url in admin panel
        """
        response = self.client.get("/admin/quickpages/quicksnippet/")
        self.assertIn("Quick snippets",response.content)
    def test_admin_customerimage(self):
        """
        Tests admin/customers/customerimage/ url in admin panel
        """
        response = self.client.get("/admin/customers/customerimage/")
        self.assertIn("Customer images",response.content)
    def test_admin_customer(self):
        """
        Tests admin/customers/customer/ url in admin panel
        """
        response = self.client.get("/admin/customers/customer/")
        self.assertIn("Customers",response.content)
    def test_admin_testimonial(self):
        """
        Tests admin/customers/testimonial/ url in admin panel
        """
        response = self.client.get("/admin/customers/testimonial/")
        self.assertIn("Testimonials",response.content)
    def test_admin_importedorder(self):
        """
        Tests admin/orders/importedorder/ url in admin panel
        """
        response = self.client.get("/admin/orders/importedorder/")
        self.assertIn("Imported orders",response.content)
    def test_admin_order(self):
        """
        Tests admin/orders/order/ url in admin panel
        """
        response = self.client.get("/admin/orders/order/")
        self.assertIn("Orders",response.content)
    def test_admin_categories(self):
        """
        Tests admin/products/categories/ url in admin panel
        """
        response = self.client.get("/admin/products/categories/")
        self.assertIn("Categories",response.content)
    def test_admin_choicecategory(self):
        """
        Tests admin/products/choicecategory/ url in admin panel
        """
        response = self.client.get("/admin/products/choicecategory/")
        self.assertIn("choicecategory",response.content)
    def test_admin_prodopt(self):
        """
        Tests admin/products/prodopt/ url in admin panel
        """
        response = self.client.get("/admin/products/prodopt/")
        self.assertEqual(response.status_code, 200)
    def test_admin_choice(self):
        """
        Tests admin/products/choice/ url in admin panel
        """
        response = self.client.get("/admin/products/choice/")
        self.assertIn("choices",response.content)
    def test_admin_option(self):
        """
        Tests admin/products/option/ url in admin panel
        """
        response = self.client.get("/admin/products/option/")
        self.assertIn("Options",response.content)
    def test_admin_product(self):
        """
        Tests admin/products/product/ url in admin panel
        """
        response = self.client.get("/admin/products/product/")
        self.assertIn("Products",response.content)
    def test_admin_catax(self):
        """
        Tests admin/catax/catax/ url in admin panel
        """
        response = self.client.get("/admin/catax/catax/")
        self.assertIn("CA Taxes",response.content)
    def test_admin_quote(self):
        """
        Tests admin/quotes/quote/ url in admin panel
        """
        response = self.client.get("/admin/quotes/quote/")
        self.assertIn("Quotes",response.content)
    def test_admin_sql(self):
        """
        Tests admin/sqls/sql/ url in admin panel
        """
        response = self.client.get("/admin/sqls/sql/")
        self.assertIn("Sqls",response.content)
    def test_admin_scripts(self):
        """
        Tests admin/webshell/script/ url in admin panel
        """
        response = self.client.get("/admin/webshell/script/")
        self.assertEqual(response.status_code, 200)
    def test_admin_address(self):
        """
        Tests admin/email_extras/address/ url in admin panel
        """
        response = self.client.get("/admin/email_extras/address/")
        self.assertIn("Addresses",response.content)
    def test_admin_keys(self):
        """
        Tests admin/email_extras/key/ url in admin panel
        """
        response = self.client.get("/admin/email_extras/key/")
        self.assertIn("Keys",response.content)
    def test_admin_tag(self):
        """
        Tests admin/taggit/tag/ url in admin panel
        """
        response = self.client.get("/admin/taggit/tag/")
        self.assertIn("Tags",response.content)



##unit test IP-ADDRESS-SAVE
class IpaddressSaveTest(TestCase):
    def setUp(self):
        user3 = User.objects.create (username="testuser3", email="testuser3@yahoo.com", password="testuser3")
        customer3 = Customer.objects.get (user=user3)
        ipaddress3 = IpAddress.objects.create (
          customer=customer3,
          ip_address='192.168.1.10',
          comments='saved subscribe user testuser3 IP-Address',
          activity='Sign-in'
        )
    
    
    def test_activity_name(self):
        ipaddress4 = IpAddress.objects.get(ip_address='192.168.1.10')
        activity5 = ipaddress4.activity
        name1 = ipaddress4.name_activity()
        self.assertEqual(activity5, name1)


class SitemapLinksTests(TestCase):
    fixtures = ['products-all.yaml', 'customers-54730.yaml', 'quickpages-all.yaml', 'home-test.yaml']

    def test_html_sitemap(self):
        "Tests that dynamic html sitemap is being delivered with no error"
        response = self.client.get ("/sitemap.html")
        self.assertEqual (response.status_code, 200)

    def test_ror_sitemap(self):
        "Tests that dynamic ror sitemap is being delivered with no error"
        response = self.client.get ("/ror.xml")
        self.assertEqual (response.status_code, 200)

    def test_xml_sitemap_and_all_links(self):
        "Tests that dynamic xml sitemap is being delivered with no errors, and that all links are good"
        response = self.client.get ("/sitemap.xml")
        self.assertEqual (response.status_code, 200)

        #doc = minidom.parse("static/sitemap.xml")
        doc = minidom.parseString (response.content)
        all_links = doc.getElementsByTagName("loc")
        for link in all_links:
            if trace:
                print "XML SITEMAP"
            time.sleep(1)
            urlpath = urlparse.urlsplit (link.firstChild.data).path
            if not urlpath.endswith ('/'):
                urlpath += '/'
            if trace:
                print link.firstChild.data
                print 'TRYING', urlpath
            response = self.client.get (urlpath)
            if response.status_code != 200:
                print 'Sitemap incorrect:', urlpath, response.status_code
            self.assertEqual(response.status_code, 200)


 
# ##social login test cases:        
class SocialLoginWithRequestTest(TestCase):
    
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()    
    
    def test_facebook_login(self):
        """
        Test for facebook login works with python social auth for eracks.com
        """
        request = self.factory.get('/register/token/facebook/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()        
        backend = 'facebook'
        response = testing_social_auth_by_access_token(request,backend)
        self.assertIn ('facebook',response.content)

    def test_github_login(self):
        
        """
        Test for github login works with python social auth for eracks.com
        """ 
        
        request = self.factory.get('/register/token/github/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()        
        backend = 'github'
        response = testing_social_auth_by_access_token(request,backend)
        self.assertIn ('github',response.content)

    # def test_linkedin_login(self):
        
    #     """
    #     Test for linkedin login works with python social auth for eracks.com
    #     """ 
    #     request = self.factory.get('/register/token/linkedin/')
    #     middleware = SessionMiddleware()
    #     middleware.process_request(request)
    #     request.session.save()        
    #     backend = 'linkedin'
    #     response = testing_social_auth_by_access_token(request,backend)
    #     self.assertIn ('linkedin',response.content)

    # def test_google_login(self):


    #     """
    #     Test for Google login works with python social auth for eracks.com
    #     """ 
        
    #     request = self.factory.get('/register/token/google-oauth2/')
    #     middleware = SessionMiddleware()
    #     middleware.process_request(request)
    #     request.session.save()        
    #     backend = 'google-oauth2'
    #     response = testing_social_auth_by_access_token(request,backend)
    #     self.assertIn ('google',response.content)

