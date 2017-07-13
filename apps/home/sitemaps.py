from collections import OrderedDict

#from django.contrib import sitemaps
from django.core.urlresolvers import reverse
from django.contrib.sitemaps import Sitemap, GenericSitemap  # FlatPageSitemap

from products.models import Product, Categories
from quickpages.models import QuickPage

class Str (unicode):  # allows setting attributes
  pass

#class TitleStr (unicode):  # allows setting attributes
#  def


#### Home page, static pages

class HomePageSitemap (Sitemap):
    priority = 1.0
    changefreq = 'daily'

    index = Str ('index')
    index.name = 'eRacks Home Page'
    index.title = 'eRacks Open Source Systems'
    index.meta_title = "Rackmount Server, Open Source Systems, Linux Rackmount"
    index.meta_description = "We are the leading Open Source Systems features its own line of rack mount server and offer a wide array of services including security and network architecture services."
    index.sortorder = '0'  # must be string otherwise it evaluates to False in template for firstof :)

    def items(self):
        return [self.index,]

    def location(self, item):
        return reverse(item)


class StaticViewSitemap (Sitemap):
    priority = 0.64
    changefreq = 'daily'
    itemlist = [Str(s) for s in ('contact', 'customers', 'user_signup', 'userena_signin', 'userena_signout')]  #'accounts/password/reset',]
    for item in itemlist:
      item.sortorder = 1

    def items(self):
        return self.itemlist

    def location(self, item):
        return reverse(item)


class StaticQuickPageSitemap (Sitemap):
    changefreq = "daily"
    priority = 0.64

    def items(self):
        return QuickPage.objects.published().exclude (template__contains='press.html').exclude (name__icontains='google')

    def lastmod(self, obj):
        return obj.updated


#### Press pages

class PressSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5120

    def items(self):
        return QuickPage.objects.filter(published=True, template__contains='press.html').exclude (name__icontains='google')

    def lastmod(self, obj):
        return obj.updated


#### Product, category pages -now in shortcut format - https://docs.djangoproject.com/en/1.7/ref/contrib/sitemaps/#shortcuts
#
#class ProductSitemap(Sitemap):
#    changefreq = "daily"
#    priority = 0.5
#
#    def items(self):
#        return Product.objects.filter(published=True)
#
#    def lastmod(self, obj):
#        return obj.updated



#### 'Exported' sitempas dicts

partial_sitemaps = OrderedDict (
    home = HomePageSitemap,
    static = StaticViewSitemap,
    quickpages=StaticQuickPageSitemap,
    #quickpages = GenericSitemap (dict (queryset=QuickPage.objects.published(),  date_field='updated'), priority=0.64),
    categories = GenericSitemap (dict (queryset=Categories.objects.published(), date_field='updated'), priority=0.8),
  )

all_sitemaps = OrderedDict (
    home = HomePageSitemap,
    static = StaticViewSitemap,
    quickpages=StaticQuickPageSitemap,
    #quickpages = GenericSitemap (dict (queryset=QuickPage.objects.published(),  date_field='updated'), priority=0.64),
    presspages=PressSitemap,
    categories = GenericSitemap (dict (queryset=Categories.objects.published(), date_field='updated'), priority=0.8),
    products   = GenericSitemap (dict (queryset=Product.objects.published(),    date_field='updated'), priority=0.8),
  )
