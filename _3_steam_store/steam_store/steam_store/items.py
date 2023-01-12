# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from scrapy.selector import Selector
from w3lib.html import remove_tags
import re



def get_platforms(platforms):
    list_platform = []
    for platform in platforms:
        item =  platform.split(' ')[1] if re.search(' ', platform) else platform
        if item == 'win':
            list_platform.append('Windows')
        if item == 'mac':
            list_platform.append('Mac Os')
        if item == 'linux':
            list_platform.append('Linux')
        if item == 'vr_supported':
            list_platform.append('Vr Supported')
    return list_platform

def remove_html(review_summary):
    cleaned_review_summary = ''
    try:
        cleaned_review_summary = remove_tags(review_summary)
    except:
        cleaned_review_summary = 'No review'
    return cleaned_review_summary

def clean_discount_rate(discounted_rate):
        return discounted_rate.lstrip('-') if discounted_rate else discounted_rate

def get_original_price(html_markup):
    origin_price = ''
    selector_obj = Selector(text=html_markup)
    span_with_discount = selector_obj.xpath('.//span/strike/text()').get()
    origin_price = span_with_discount if span_with_discount else selector_obj.xpath('normalize-space(.//text())').get()
    return origin_price



class SteamStoreItem(scrapy.Item):
    game_url = scrapy.Field(
        output_processor = TakeFirst()
    )
    image_url = scrapy.Field(
        output_processor = TakeFirst()
    )
    game_name = scrapy.Field(
        output_processor = TakeFirst()
    )
    release_date = scrapy.Field(
        output_processor = TakeFirst()
    )
    platform = scrapy.Field(
        input_processor = MapCompose(get_platforms),
        output_processor = Join('')
    )
    review_summary = scrapy.Field(
        input_processor = MapCompose(remove_html),
        output_processor = TakeFirst()
    )
    original_price = scrapy.Field(
        input_processor = MapCompose(get_original_price),
        output_processor = TakeFirst()
    )
    discounted_rate = scrapy.Field(
        input_processor = MapCompose(clean_discount_rate),
        output_processor = TakeFirst()
    )
