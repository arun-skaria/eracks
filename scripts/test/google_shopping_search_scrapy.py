import scrapy

class GoogleShoppingSpider (scrapy.Spider):
    name = 'gshopspider'
    start_urls = ['https://www.google.com/search?q=WD+Black+internal+drives&tbm=shop']

    def parse(self, response):
        for title in response.css('div.pslicont'):
            yield {'title': title.css('a ::text').extract_first()}

        next_page = 0 # response.css('div.prev-post > a ::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

