import json
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from w3lib.http import basic_auth_header
import scrapy


class IndexSpider(scrapy.Spider):
    http_user = 'user'
    http_pass = 'userpass'
    name = 'index'
    init_url = 'https://www.bucataras.ro/'

    def start_requests(self):
        for i in range(len(1,5)):
            yield SplashRequest(
                url = f"https://www.bucataras.ro/retete/mincare-de-post/?p={i}",
                callback = self.find_recipe_list,
                splash_headers={'Authorization':basic_auth_header('user','userpass')}
            )

    def find_recipe_list(self,response):
        recipes = response.xpath('//div[@class="cat-row clearfix"]/div[@class="shaded-box fl"]')
        for recipe in recipes:
            url = recipe.xpath('.//div/div/a')
            yield {
                'Nghi': url
            }
            # yield SplashRequest(
            #     url = f"{self.init_url}{url}",
            #     callback = self.parse,
            #     splash_headers={'Authorization':basic_auth_header('user','userpass')}
            # )

    # def parse(self, response):
    #     people = response.xpath('//div[@class="cfs-attendees-grid-item"]')
    #     for person in people:
    #         name = person.xpath('./div/div[2]/div/h3/text()').get()
    #         company = person.xpath('./div/div[2]/div/p[1]/text()').get()
    #         yield {
    #             'Name': name,
    #             'Company': company,
    #         }
