# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

import re

from scrapy.item import Item, Field

from scrapy.contrib.loader.processor import MapCompose, Identity, Join, TakeFirst

from scrapy.utils.markup import remove_entities

class CatalogueItem(Item):

    def filter_euro(x):
        return re.sub(ur'[\u20ac]','', x)

    name = Field()
    image_src = Field()
    url = Field()
    price = Field(
        input_processor=MapCompose(filter_euro, unicode.strip),
    )
    details = Field(
        input_processor=MapCompose(unicode.strip),
    )
    catalogue_number = Field()

class CategoryItem(Item):
    name = Field(
        input_processor=MapCompose(unicode.strip),
        output_processor=Join(),
    )
    sub_categories = Field()
