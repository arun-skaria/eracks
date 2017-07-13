# start_urls = ['https://www.google.com/search?q=WD+Black+internal+drives&tbm=shop']
# for title in response.css('div.pslicont'):

import demiurge

class GoogleShoppingItem (demiurge.Item):
    #url = demiurge.AttributeValueField (selector='td:eq(2) a:eq(1)', attr='href')
    #name = demiurge.TextField(selector='td:eq(2) a:eq(2)')
    #size = demiurge.TextField(selector='td:eq(3)')
    heading = demiurge.TextField(selector='.pslmain h3')
    image = demiurge.AttributeValueField (selector='.pslimg img', attr='alt')
    price = demiurge.TextField(selector='.pslline price')
    main  = demiurge.TextField(selector='.pslmain')

    class Meta:
        selector = '.pslicont' #'table.maintable:gt(0) tr:gt(0)'
        base_url = 'https://www.google.com'  #'http://www.mininova.org'

results = GoogleShoppingItem.all ('/search?q=WD+Black+internal+drives&tbm=shop')
print len(results)
print results

