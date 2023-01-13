import scrapy
from ..utils import URL, cookie_parser, parse_new_url
from ..items import ZillowItem
from scrapy.loader import ItemLoader
import json



class IndexSpider(scrapy.Spider):
    name = 'index'
    allowed_domains = ['www.zillow.com']
  

    def start_requests(self):
        yield scrapy.Request(
            url = URL,
            callback = self.parse,
           cookies = cookie_parser(),
           meta = {
            'currentPage' : 1
           } 
        )

    def parse(self, response):
        current_page = response.meta['currentPage']

        json_resp = json.loads(response.body)
        houses = json_resp.get('cat1').get('searchResults').get('listResults')

        for house in houses:

            loader = ItemLoader(item=ZillowItem())
            loader.add_value('id', house.get('id'))
            loader.add_value('image_urls', house.get('imgSrc'))
            loader.add_value('detailUrl', house.get('detailUrl'))
            loader.add_value('statusType', house.get('statusType'))
            loader.add_value('statusText', house.get('statusText'))
            loader.add_value('address', house.get('address'))
            loader.add_value('beds', house.get('beds'))
            loader.add_value('baths', house.get('baths'))
            loader.add_value('area', house.get('area'))
            loader.add_value('price', house.get('price'))
            loader.add_value('latitude', house.get('latLong').get('latitude'))
            loader.add_value('longitude', house.get('latLong').get('longitude'))
            loader.add_value('brokerName', house.get('brokerName'))

            yield loader.load_item()

        total_pages = json_resp.get('cat1').get('searchList').get('totalPages')
        # if current_page <= total_pages:
        #     current_page += 1
        #     yield scrapy.Request(
        #         url = parse_new_url(URL, current_page),
        #         callback = self.parse,
        #         cookies = cookie_parser(),
        #         meta = {
        #             'currentPage': current_page
        #         }
        #     )