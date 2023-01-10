import scrapy
from scrapy.loader import itemloaders
from ..items import SteamStoreItem
import re
from w3lib.html import remove_tags

class IndexSpider(scrapy.Spider):
    name = 'index'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/search/?filter=topsellers']

    def get_platforms(self, platforms):
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

    def remove_html(self, review_summary):
        cleaned_review_summary = ''
        try:
            cleaned_review_summary = remove_tags(review_summary)
        except:
            cleaned_review_summary = 'No review'
        return cleaned_review_summary

    def clean_discount_rate(self,discounted_rate):
            return discounted_rate.lstrip('-') if discounted_rate else discounted_rate

    def get_original_price(self,selector_obj):
        origin_price = ''
        span_with_discount = selector_obj.xpath('.//span/strike/text()').get()
        origin_price = span_with_discount if span_with_discount else selector_obj.xpath('normalize-space(.//text())').get()
        return origin_price

    def parse(self, response):
        steam_item = SteamStoreItem()
        games = response.xpath('//div[@id="search_resultsRows"]/a')
        for game in games:
 


            steam_item['game_url'] = game.xpath('.//@href').get()
            steam_item['image_url'] = game.xpath('.//div[@class="col search_capsule"]/img/@src').get()
            steam_item['game_name'] = game.xpath('.//div[@class="responsive_search_name_combined"]/div[1]/span/text()').get()
            steam_item['release_date'] = game.xpath('.//div[@class="col search_released responsive_secondrow"]/text()').get()
            steam_item['platform'] = self.get_platforms(game.xpath('.//span[contains(@class,"platform_img") or @class="vr_supported"]/@class').getall())    
            steam_item['review_summary'] = self.remove_html(game.xpath('.//span[contains(@class,"search_review_summary ")]/@data-tooltip-html').get())
            steam_item['original_price'] = self.get_original_price(game.xpath('.//div[@class="col search_price_discount_combined responsive_secondrow"]/div[contains(@class,"col search_price")]'))
            steam_item['discounted_rate'] = self.clean_discount_rate(game.xpath('.//div[@class="col search_discount responsive_secondrow"]/span/text()').get())

            yield steam_item

