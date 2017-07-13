from django.conf import settings
from django.test import TestCase, LiveServerTestCase
from django.test import Client
from django.contrib.auth.models import User, Group

# nope, times out
#from django.contrib.staticfiles.testing import StaticLiveServerTestCase

trace = 1

try:
    from selenium import webdriver
    if trace:
        print 'SELENIUM PRESENT'
        import os
        print os.environ
except:
    webdriver = False


class ViewsTests (TestCase):
    def setUp(self):
            user1 = User.objects.create_superuser (username="admin_eracks", email="admin_eracks@eracks.com", password="admin_eracks")

    def test_urls(self):
        client = Client()
        response1 = client.post("/accounts/login/", {'identification': 'admin_eracks', 'password': 'admin_eracks'})
        #if trace: print 'RESPONSE1', response1
        response = client.get("/utils/urls/")
        #if trace: print 'RESPONSE', response
        self.assertEqual(response.status_code, 200)

    def test_clearcache(self):
        client = Client()
        response = client.get("/utils/clearcache")
        #if trace: print 'RESPONSE', response
        self.assertEqual(response.status_code, 200)


# TODO: Migrate ones using this to use the in-class version (and test)
def find_first(selenium, *selector_list):
    for sel in selector_list:
        try:
            elm = selenium.find_element_by_css_selector (sel)
            return elm
        except Exception,e:
            if trace:
                if e: print 'Selector Exception:', e
    raise Exception ("No selector matches")

class SelectorException (Exception):
    pass

def drivers_present():
    return webdriver and (settings.USEFIREFOX or settings.USECHROME)


def get_drivers():
    if not webdriver: return []

    drivers = []

    if settings.USEFIREFOX:
        if trace: print 'USING FIREFOX FOR TESTING'
        drivers.append (webdriver.Firefox())

    if settings.USECHROME:
        if trace: print 'USING CHROME FOR TESTING'
        chrome_options = webdriver.chrome.options.Options()
        chrome_options.add_argument('--dns-prefetch-disable')
        drivers.append (webdriver.Chrome (executable_path = settings.CHROME_DRIVER_PATH, chrome_options = chrome_options))

    if trace: print 'USING', drivers

    return drivers


def test_drivers (driver_pool='drivers'):
    import functools

    def wrapped(test_func):
        @functools.wraps(test_func)
        def decorated(test_case, *args, **kwargs):
            test_class = test_case.__class__
            web_driver_pool = getattr(test_class, driver_pool)
            if trace:
                print 'RUNNING TEST', test_class, test_case, ' WITH ', driver_pool
            for web_driver in web_driver_pool:
                setattr(test_case, 'selenium', web_driver)
                test_func(test_case, *args, **kwargs)
        return decorated
    return wrapped


class MyLiveTestCase (LiveServerTestCase):
    selenium = None
    drivers = []
    display = None

    @classmethod
    def setUpClass(cls):
        if settings.USEVIRTUALDISPLAY:
            if trace:
                print 'USING VIRTUAL FRAMEBUFFER DISPLAY'
            from pyvirtualdisplay import Display
            cls.display = Display (visible=0, size= (1600, 1200))  # (1366, 768))
            cls.display.start()

        cls.drivers = get_drivers()  # [webdriver.Chrome (executable_path=settings.CHROME_DRIVER_PATH), webdriver.Firefox()]

        super (MyLiveTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super (MyLiveTestCase, cls).tearDownClass()

        for d in cls.drivers:
          d.quit()

        if cls.display:
            cls.display.stop()

    def find_first (self, *selector_list):
        for sel in selector_list:
            try:
                elm = self.selenium.find_element_by_css_selector (sel)
                return elm
            except Exception,e:
                if trace:
                    if e: print 'Selector Exception:', e
        raise SelectorException ("No selector matches")

    def screengrabs (self, fname):
        if self.selenium.name=='chrome':
            self.selenium.get_screenshot_as_file ('media/test_results_screens/chrome/' + fname)
        if self.selenium.name=='firefox':
            self.selenium.get_screenshot_as_file('media/test_results_screens/firefox/' + fname)
