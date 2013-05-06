from scrapy.spider import BaseSpider
from scrapy.contrib.loader import XPathItemLoader
from scrapy.selector import HtmlXPathSelector

from scrape_argos.items import CategoryItem 

class ArgosGroupSpider(BaseSpider):
    name = "argos"
    allowed_domains = ["argos.ie"]
    start_urls = [
        "http://www.argos.ie"
    ]
    src_path=".//div[@id='outerwrap']" 
    categories_path=".//ul[@class='mainnavcategories navitems']/li[*]"
    sub_categories_path = ".//div[@id='dropdownmenus']/div[*]"


    def parse(self, response):

        hxs = HtmlXPathSelector(response)

        src = hxs.select(self.src_path)

        sub_categories = src.select(self.sub_categories_path)

        subs = {}
        for s in sub_categories:
            code = ''.join(s.select("@id").extract())
            num_li = len(list(s.select("ul/li").extract()))
            groups=[]
            while num_li > 0:
                li = s.select("ul/li[%s]" % num_li)
                num_h2 = len(list(li.select("h2")))
                while num_h2 > 0:
                    group={}
                    group['name'] = ''.join(li.select("h2[%s]/text()" % num_h2).extract())
                    link_groups = li.select("h2[%s]/following-sibling::ul[1]/li" % num_h2)
                    links=[]
                    for link_group in link_groups:
                        test = {}
                        test['name'] = link_group.select("a/text()").extract()
                        test['url'] = link_group.select("a/@href").extract()
                        links.append(test)
                    group['sub_categories'] = links
                    groups.append(group)
                    num_h2 -= 1
                num_li -= 1
            subs[code] = groups

        categories = src.select(self.categories_path)
        for category in categories:
            code = ''.join(category.select("@rel").extract())
            l = XPathItemLoader(CategoryItem(), category)
            l.add_xpath('name', "a/span/span/text()")
            l.add_value('sub_categories', subs[code])
            yield l.load_item()

