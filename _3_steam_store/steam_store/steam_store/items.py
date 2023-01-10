# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SteamStoreItem(scrapy.Item):
    game_url = scrapy.Field()
    image_url = scrapy.Field()
    game_name = scrapy.Field()
    release_date = scrapy.Field()
    platform = scrapy.Field()
    review_summary = scrapy.Field()
    original_price = scrapy.Field()
    discounted_rate = scrapy.Field()
