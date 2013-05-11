from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.spiders import XMLFeedSpider
from scrapy.http import Request

from scrape_argos.items import CatalogueItem


class ArgosSpider(XMLFeedSpider):
    """
    A spider that crawls the argos.ie products sitemap and returns
    CatalogueItems in a format that's easily indexed.
    """

    name = "argos"
    allowed_domains = ["argos.ie"]
    start_urls = [
        "http://www.argos.ie/product.xml"
    ]

    # sitemap
    namespaces = [('n', 'http://www.sitemaps.org/schemas/sitemap/0.9')]
    itertag = 'n:loc'

    # catalogue item xpaths
    name_path = ".//*[@id='primaryproductinfo']/h1/text()"
    catalogue_number_path = ".//*[@id='primaryproductinfo']/span/text()"
    price_path = ".//*[@id='pdpForm']/div[2]/ul/li[2]/span/text()[1]"
    image_src_path = ".//*[@id='mainimage']/@src"
    details_path = ".//*[@id='producttabs']/div[1]"

    def make_requests_from_url(self, url):
        """
        Overrides the BaseSpider class in order to set the dont_redirect
        Request meta.
        The argos products sitemap contains a lot of links that return 302
        and redirect to a search page. Not following these reduces the crawl
        overhead.
        """
        return Request(
            url,
            meta={'dont_redirect': True},
            dont_filter=True
        )

    def parse_node(self, response, selector):
        """
        Implements the XMLFeedSpider parse_node.
        Parses argos.ie catalogue pages and scrapes Items.
        """
        l = XPathItemLoader(
            item=CatalogueItem(),
            response=response
        )
        l.add_xpath('name', self.name_path)
        l.add_xpath('catalogue_number', self.catalogue_number_path)
        l.add_xpath('price', self.price_path)
        l.add_xpath('image_src', self.image_src_path)
        l.add_xpath('details', self.details_path)
        l.add_value('url', response.url)
        return l.load_item()