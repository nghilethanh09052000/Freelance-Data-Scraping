import scrapy
from scrapy.loader import ItemLoader
from ..items import SteamStoreItem


class IndexSpider(scrapy.Spider):
    name = 'index'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/search/?filter=topsellers/']


    def parse(self, response):
        steam_item = SteamStoreItem()
        games = response.xpath('//div[@id="search_resultsRows"]/a')
        for game in games:

            loader = ItemLoader(item = SteamStoreItem(), selector = game, response = response)
            loader.add_xpath('game_url','.//@href')
            loader.add_xpath('image_url','.//div[@class="col search_capsule"]/img/@src')
            loader.add_xpath('game_name','.//div[@class="responsive_search_name_combined"]/div[1]/span/text()')
            loader.add_xpath('release_date','.//div[@class="col search_released responsive_secondrow"]/text()')
            loader.add_xpath('platform','.//span[contains(@class,"platform_img") or @class="vr_supported"]/@class')
            loader.add_xpath('review_summary','.//span[contains(@class,"search_review_summary ")]/@data-tooltip-html')
            loader.add_xpath('original_price','.//div[@class="col search_price_discount_combined responsive_secondrow"]/div[contains(@class,"col search_price")]')    
            loader.add_xpath('discounted_rate','.//div[@class="col search_discount responsive_secondrow"]/span/text()')

            # steam_item['game_url'] = game.xpath('.//@href').get()
            # steam_item['image_url'] = game.xpath('.//div[@class="col search_capsule"]/img/@src').get()
            # steam_item['game_name'] = game.xpath('.//div[@class="responsive_search_name_combined"]/div[1]/span/text()').get()
            # steam_item['release_date'] = game.xpath('.//div[@class="col search_released responsive_secondrow"]/text()').get()
            # steam_item['platform'] = self.get_platforms(game.xpath('.//span[contains(@class,"platform_img") or @class="vr_supported"]/@class').getall())    
            # steam_item['review_summary'] = self.remove_html(game.xpath('.//span[contains(@class,"search_review_summary ")]/@data-tooltip-html').get())
            # steam_item['original_price'] = self.get_original_price(game.xpath('.//div[@class="col search_price_discount_combined responsive_secondrow"]/div[contains(@class,"col search_price")]'))
            # steam_item['discounted_rate'] = self.clean_discount_rate(game.xpath('.//div[@class="col search_discount responsive_secondrow"]/span/text()').get())

            yield loader.load_item()

        next_page = response.xpath('//a[@class="pagebtn" and text()=">"]/@href').get()
        # if next_page:
        #     yield scrapy.Request(
        #         url = next_page,
        #         callback = self.parse,
        #     )
        #http://localhost:9080/crawl.json?start_requests=true&spider_name=index

