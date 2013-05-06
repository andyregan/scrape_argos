from scrapy.contrib.loader import XPathItemLoader
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector, XmlXPathSelector
from scrapy.spider import BaseSpider

from scrape_argos.items import CatalogueItem 

class ArgosSpider(BaseSpider):
    name = "argos"
    allowed_domains = ["argos.ie"]
    start_urls = [
        "http://www.argos.ie/product.xml"
    ]

    # sitemap
    namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
    item_url_path = "//n:loc/text()"

    # catalogue item
    name_path = ".//*[@id='primaryproductinfo']/h1/text()"
    catalogue_number_path = ".//*[@id='primaryproductinfo']/span/text()"
    price_path = ".//*[@id='pdpForm']/div[2]/ul/li[2]/span/text()[1]"
    image_src_path = ".//*[@id='mainimage']/@src"
    details_path = ".//*[@id='producttabs']/div[1]"

    def parse(self, response):
        xxs = XmlXPathSelector(response)
        xxs.register_namespace('n', self.namespace)
        links = xxs.select(self.item_url_path).extract()
        return [Request(x, callback=self.parse_item) for x in links]

    def parse_item(self, response):
	l = XPathItemLoader(item=CatalogueItem(), response=response)
        l.add_xpath('name', self.name_path) 
        l.add_xpath('catalogue_number', self.catalogue_number_path)
        l.add_xpath('price', self.price_path)
        l.add_xpath('image_src', self.image_src_path)
        l.add_xpath('details', self.details_path)
        return l.load_item()
