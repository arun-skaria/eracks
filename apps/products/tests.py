"""
These are the tests for the products app.

These will pass (or not!) when you run "manage.py test".
"""

import unittest, time

from django.test import TestCase, Client
from django.contrib.auth.models import User  #, Group

from products.models import *
from utils.tests import find_first, drivers_present, test_drivers, MyLiveTestCase

trace = 1
breakpoint = 0

if drivers_present():
    class LiveProductTest (MyLiveTestCase):
        fixtures = ['products-all.yaml',]  # TODO: Add pre-dump of temp fixtures & cycle through products for production db!

        @test_drivers()
        def test_product_grid (self):
            for prod in 'NAT', 'DMZ':  # could loop thru published prods here, but then not through all the opts/choices
                response1 = self.selenium.get ('%s%s' % (self.live_server_url, "/products/firewall-servers/%s/#config" % prod))
                time.sleep (2)

                if breakpoint:
                  from IPython import embed
                  embed()  # breaks into an ipython shell here!

                ## See also home/management/commands/test_production_livedb - this is taken from there
                base_price = self.selenium.find_element_by_css_selector ('#config_summary #current .baseprice b').text
                price_before = self.selenium.find_element_by_css_selector ('#config_summary #current .price b').text

                if trace:
                    print 'BASE PRICE, PRICE BEFORE', base_price, price_before

                ## Get rows, iterate through options (rows) & choices (opts)
                sels = self.selenium.find_elements_by_css_selector ("table.configgrid tr td select")
                for sel in sels:
                  for opt in sel.find_elements_by_tag_name ("option"):
                    opt.click()

                ## Check new price
                price_after = self.selenium.find_element_by_css_selector ('#config_summary #current .price b').text

                if trace:
                    print 'PRICE AFTER', price_after

                self.screengrabs ('test_product_grid_%s.png' % prod)
                self.assertNotEqual (price_after, price_before)



class FixturesTest(TestCase):
    fixtures = ['products-all.yaml']  # DMZ model - pulls in firewall-servers category, all opts/choices/choicecats

    def test_products_fixtures(self):
        p = Product.objects.get(pk=2)  # 3)
        self.assertTrue(p)


class ViewsTests(TestCase):
    fixtures = ['quickpages.yaml', 'products-all.yaml']

    def test_showroom(self):  # requires loaded product category(ies)
        client = Client()
        response = client.get("/products/categories/")  # showroom/")
        self.assertEqual(response.status_code, 200)

    def test_press(self):  # requires loaded quickpages
        client = Client()
        response = client.get("/press/")  # really not a product test..
        self.assertEqual(response.status_code, 200)

    def test_category(self):  # requires loaded product category
        client = Client()
        response = client.get("/products/firewall-servers/")
        self.assertEqual(response.status_code, 200)


class ProductApiTests(TestCase):
    def setUp(self):
        categories1 = Categories.objects.create (name='lapi', slug='lapi', title='lapi')
        categoryimage1 = CategoryImage.objects.create (
          image='images/categories/intel-systems/corei7_75.jpeg',
          title='My Category',
          caption='My Caption',
          category=categories1
        )
        choicecategory1 = ChoiceCategory.objects.create (name='lapis', sohigh=2255, solow=2500)
        choice1 = Choice.objects.create (
          name='lapi',
          source='',
          price=0,
          cost=246.56,
          sortorder=222,
          multiplier=2,
          choicecategory=choicecategory1
        )
        option1 = Option.objects.create (name='laptops', usage_notes='all laptops', sortorder=222)
        product1 = Product.objects.create (
          name='mylapi',
          sku='mylapi',
          baseprice=2500.55,
          cost=2500.00,
          category=categories1,
          weight=20,
          sortorder=222
        ) #, multiplier=2)
        productimage1 = ProductImage.objects.create (
          image='images/products/zenbook/zenbook_3.jpeg',
          title='lapi',
          caption='lapi',
          product=product1
        )
        prodopt1 = Prodopt.objects.create (
          name='mylapi',
          qty=1,
          choices_orderby='cost',
          product=product1,
          option=option1,
          defaultchoice=choice1
        )

    def test_cat_image_tag(self):
        image1 = CategoryImage.objects.get(title='My Category')
        self.assertTrue(image1.tag())

    def test_prod_image_tag(self):
        image1 = ProductImage.objects.get(title='lapi')
        self.assertTrue(image1.tag())

    def test_get_absolute_url(self):
        categories1 = Categories.objects.get(slug='lapi')
        self.assertTrue(categories1.get_absolute_url())

    def test_prods_as_divs(self):
        categories1 = Categories.objects.get(slug='lapi')
        self.assertTrue(categories1.prods_as_divs())

    def test_calc_markup(self):
        choice1 = Choice.objects.get(name='lapi')
        self.assertTrue(choice1.calc_markup)

    def test_calc_price(self):
        choice1 = Choice.objects.get(name='lapi')
        self.assertTrue(choice1.calc_price)

    def test_url(self):
        product1 = Product.objects.get(name='mylapi')
        self.assertTrue(product1.url)

    def test_slug(self):
        product1 = Product.objects.get(name='mylapi')
        self.assertTrue(product1.slug)

    def test_product_options(self):
        product1 = Product.objects.get(name='mylapi')
        self.assertTrue(product1.product_options())

    def test_calc_description(self):
        product1 = Product.objects.get(name='mylapi')
        self.assertTrue(product1.calc_description)

    def test_calc_specs(self):
        product1 = Product.objects.get(name='mylapi')
        self.assertTrue(product1.calc_specs)

    def test_prodopts_as_table(self):
        product1 = Product.objects.get(name='mylapi')
        self.assertTrue(product1.prodopts_as_table)

# Removed 10/14/15 JJW - TODO: check and make new tests for the new models, fields, and functions I added to products
#
#    def test_as_content(self):
#        product1 = Product.objects.get(name='mylapi')
#        self.assertTrue(product1.as_content)

    def test_calc_relative_price(self):
        prodopt1 = Prodopt.objects.get(name='mylapi')
        choice1 = Choice.objects.get(name='lapi')
        self.assertFalse(prodopt1.calc_relative_price(choice1))

    def test_choice_name_and_price(self):
        prodopt1 = Prodopt.objects.get(name='mylapi')
        choice1 = Choice.objects.get(name='lapi')
        self.assertTrue(prodopt1.choice_name_and_price(choice1))

    def test_calc_name(self):
        prodopt1 = Prodopt.objects.get(name='mylapi')
        self.assertTrue(prodopt1.calc_name)

    def test_option_choices(self):
        prodopt1 = Prodopt.objects.get(name='mylapi')
        self.assertFalse(prodopt1.option_choices())

    def test_all_choices(self):
        prodopt1 = Prodopt.objects.get(name='mylapi')
        self.assertFalse(prodopt1.all_choices())
