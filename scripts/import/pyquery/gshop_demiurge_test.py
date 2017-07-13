# start_urls = ['https://www.google.com/search?q=WD+Black+internal+drives&tbm=shop']
# for title in response.css('div.pslicont'):

import demiurge
from time import sleep


class ItemPriceDetailRow (demiurge.Item):
    #url    = demiurge.AttributeValueField (selector='.pslires .psliimg img', attr='href')
    seller  = demiurge.TextField (selector="td.os-seller-name")
    rating  = demiurge.AttributeValueField (selector="td.os-rating-col span div[aria-label]", attr="aria-label" )
    votes   = demiurge.TextField (selector="td.os-rating-col a")
    details = demiurge.TextField (selector="td.os-details-col")
    price   = demiurge.TextField (selector="td.os-price-col span.os-base_price")
    total   = demiurge.TextField (selector="td.os-total-col")

    class Meta:
        selector = 'tr.os-row'


class GoogleShoppingItem (demiurge.Item):
    #url = demiurge.AttributeValueField (selector='td:eq(2) a:eq(1)', attr='href')
    #name = demiurge.TextField(selector='td:eq(2) a:eq(2)')
    #size = demiurge.TextField(selector='td:eq(3)')

    heading = demiurge.TextField(selector='.pslires h3')  #'.pslmain h3')
    image   = demiurge.AttributeValueField (selector='.pslires .psliimg img', attr='alt')
    link    = demiurge.AttributeValueField (selector='.pslires h3 a', attr='href')
    price   = demiurge.TextField(selector='.pslires div b:contains("$")')  #'.pslline price') # best price, usually 30-40% lower than avg
    rows    = demiurge.RelatedItem (ItemPriceDetailRow, selector=".pslires h3 a", attr="href")
    #main   = demiurge.TextField(selector='.pslmain')

    class Meta:
        #selector = '.pslicont' #'table.maintable:gt(0) tr:gt(0)'
        selector = '.pslires' #'table.maintable:gt(0) tr:gt(0)'
        base_url = 'https://www.google.com'  #'http://www.mininova.org'


results = GoogleShoppingItem.all ('/search?q=WD+Black+internal+drives&tbm=shop')
print len(results)
#print results

import numpy

for r in results:
  #print r.image
  #print r.heading  # ascii error
  sleep (1)
  print r.price, r.link
  prices = []
  for row in r.rows:
    prices += [row.total]
    print '  ', row.seller, row.price, row.total, row.rating, row.votes
    prices = [p if type (p) == float else p.strip ('$') for p in prices]
    prices = [float (p) for p in prices]
    print 'Mean', numpy.mean (prices)
    print 'Std', numpy.std (prices)
  print
