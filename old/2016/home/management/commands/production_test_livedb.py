import unittest
import random
import string
import time

from django.core.management.base import BaseCommand
from django.test import TestCase, Client
from django.conf import settings
from django.contrib.auth.models import User, Group

from home.models import *
from customers.models import *
from products.models import *

from selenium import webdriver
#from selenium.webdriver.common.action_chains import ActionChains

# DANGEROUS! Be carefulhere: using MyLiveTestCase ATTEMPTS FLUSH OF PROD DB!
#from utils.tests import find_first, drivers_present, test_drivers, MyLiveTestCase

trace = 0
breakpoint = 0
timeout = 3

class Command (BaseCommand):
    help = """
    Run the test cases against the live database - loop through product options & choices and select them.

    DEPRECATED: use product unit tests, with fixtures.
    TODO: localized version which accesses locally configured DB, and doesn't flush!
    """

    def handle (self, **options):
        suite = unittest.defaultTestLoader.loadTestsFromTestCase (LiveProductionTest)
        unittest.TextTestRunner().run(suite)

#if drivers_present():
class LiveProductionTest (unittest.TestCase):  # (MyLiveTestCase - SEE NOTE ABOVE):
    selenium = None

    @classmethod
    def setUpClass(cls):
        cls.selenium = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()


    # @unittest.skip("This is getting: a 302 instead of 200 - SSL issue?")
    def production_test_choices(self):

        print '''
        This command-based test is DEPRECATED.  It accesses the production website, no matter where it's run!
        TODO: Localized version which accesses locally configured DB, and doesn't flush!
        '''

        # TODO: Localized version which accesses locally configured DB, and doesn't flush!
        # here's where you woul dloop through published products, and use a subclass of LiveServerTestCase,
        # CAREFULLY modified to NOT flush the db!  See _fixturesSetup and _FixturesTeardown, etc.

        ## Start with NAT model, jump to configurator (or tab, in Legacy)
        self.selenium.get('https://eracks.com/products/firewall-servers/NAT/#config')
        time.sleep(timeout)

        ## Get prices
        base_price = self.selenium.find_element_by_css_selector ('#config_summary #current .baseprice b').text
        price_before = self.selenium.find_element_by_css_selector ('#config_summary #current .price b').text

        if trace:
            print 'BASE PRICE, PRICE BEFORE', base_price, price_before

        ## Get rows, iterate through options (rows) & choices (opts)
        # old:
        #rows = self.selenium.find_elements_by_css_selector ("table.configgrid tr")
        #for i, row in enumerate (rows):   #for row in (1,2,3,4,5):
        #  sel = self.selenium.find_element_by_css_selector ("table.configgrid tr:nth-child(%i) td select" % (i+1))

        sels = self.selenium.find_elements_by_css_selector ("table.configgrid tr td select")
        for sel in sels:
          for opt in sel.find_elements_by_tag_name ("option"):
            opt.click()

        if breakpoint:
          from IPython import embed
          embed()  # breaks into an ipython shell here!

        ## Check new price
        price_after = self.selenium.find_element_by_css_selector ('#config_summary #current .price b').text

        if trace:
            print 'PRICE AFTER', price_after

        self.assertNotEqual(price_after, price_before)
