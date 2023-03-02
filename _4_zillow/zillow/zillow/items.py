# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst

class ZillowItem(scrapy.Item):

    id = scrapy.Field(
        output_processor = TakeFirst()
    )

    imgSrc = scrapy.Field(
        output_processor = TakeFirst()
    )
    # image_urls = scrapy.Field()
    # images = scrapy.Field()

    detailUrl = scrapy.Field(
        output_processor = TakeFirst()
    )
    statusType = scrapy.Field(
        output_processor = TakeFirst()
    )
    statusText = scrapy.Field(
        output_processor = TakeFirst()
    )
    address = scrapy.Field(
        output_processor = TakeFirst()
    )
    beds = scrapy.Field(
        output_processor = TakeFirst()
    )
    baths = scrapy.Field(
        output_processor = TakeFirst()
    )
    area = scrapy.Field(
        output_processor = TakeFirst()
    )
    price = scrapy.Field(
        output_processor = TakeFirst()
    )
    latitude = scrapy.Field(
        output_processor = TakeFirst()
    )
    longitude = scrapy.Field(
        output_processor = TakeFirst()
    )
    brokerName = scrapy.Field(
        output_processor = TakeFirst()
    )
   
