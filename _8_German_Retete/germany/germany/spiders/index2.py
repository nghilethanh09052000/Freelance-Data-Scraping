import scrapy
import json
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from w3lib.http import basic_auth_header
import scrapy
import re

class IndexSpider(scrapy.Spider):
    #71227
    http_user = 'user'
    http_pass = 'userpass'
    name = 'index2'

    init_url = 'https://www.gutekueche.at'

    recipe_route = 'cocktailkategorien'

    all_recipe_route = 'alle-rezepte'


    def start_requests(self):
        yield SplashRequest(
            url = f"{self.init_url}/{self.recipe_route}",
            callback = self.find_category,
            splash_headers={'Authorization':basic_auth_header('user','userpass')},
            args={"wait" : 3},
        )
    
    def find_category(self, response):
        recipe_list = response.xpath('//div[@class="quicklinks-grid quicklinks"]/ul/li/a/@href')
        for recipe in recipe_list:
            recipe_url = f'''{self.init_url}{recipe.get().split("-")[0]}-{self.all_recipe_route}'''
            yield SplashRequest(
                url = recipe_url,
                callback = self.list_recipe,
                args={"wait" : 2},
                meta =  {
                    'url': recipe_url
                }
            )

    def list_recipe(self, response):
        list_recipe = response.xpath('//div[@class="col "]')
        for recipe in list_recipe:
            url = recipe.xpath('.//div/div/div[2]/h3/a/@href').get()
            yield {
                'Url': f"{self.init_url}{url}",
            }

        next_page = response.xpath("//li[contains(@class,'arrow')][last()]/a/@href").get()
        if next_page:
            recipe_url = f"{self.init_url}{next_page}"
            yield SplashRequest(
                    url = recipe_url,
                    callback = self.list_recipe,
                    args={"wait" : 2},
                     meta =  {
                        'url': recipe_url
                    } 
                )

