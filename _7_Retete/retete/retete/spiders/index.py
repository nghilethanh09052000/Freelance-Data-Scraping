import json
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from w3lib.http import basic_auth_header
import scrapy
import re

class IndexSpider(scrapy.Spider):
    http_user = 'user'
    http_pass = 'userpass'
    name = 'index'

    init_url = 'https://www.bucataras.ro'
    def start_requests(self):
        null_ingredient_list = [
           'https://www.bucataras.ro/retete/sarmalute-din-orez-5882.html'
        ]
        for i in null_ingredient_list:
            yield SplashRequest(
                url = i,
                callback = self.parse,
                splash_headers={'Authorization':basic_auth_header('user','userpass')},
                args={"wait" : 3},
                meta = {
                    'url': i
                } 
            )
       
    # def find_recipe_list(self,response):
    #     recipes = response.xpath('//div[@class="cat-row clearfix"]/div[@class="shaded-box fl"]')
    #     for recipe in recipes:
    #         url = recipe.xpath('.//div/div/a/@href').get()
    #         yield SplashRequest(
    #             url = f"{self.init_url}{url}",
    #             callback = self.parse,
    #             splash_headers={'Authorization':basic_auth_header('user','userpass')},
    #             args={"wait" : 3},
    #             meta = {
    #                 'url': f"{self.init_url}{url}",
    #                 'page': response.meta['page']
    #             }
    #         )

    def parse(self, response):  
            url = response.meta['url']
            title = response.xpath('//h1[@class="main-title fw400"]/a/text()').get()
            image = f'''{self.init_url}{response.xpath('//div[@class="big-media"]/a/img/@src').get()}'''
            content = self.processing_content(response.xpath('//p[@class="mb20"]/text()'))
            ingredients = self.processing_ingredient(response.xpath('//div[@class="ingrediente __content"]/ul/p'))
            portion = response.xpath('normalize-space(//div[@class="portii-timp clearfix"]/div[1]/text())').get()
            cooking_time = self.processing_cooking_time(response.xpath('normalize-space(//div[@class="portii-timp clearfix"]/div[2]/text())').get())
            recipe_yield = self.processing_recipe_yield(response.xpath('//div[@class="rete-tips"]/div[@class="clearfix"]'))

            yield {
                'Url': url,
                'Title': title,
                'Image': image,
                'Content': content,
                'Ingredients': ingredients,
                'Portion': portion,
                'Cooking Time': cooking_time,
                'Recipe Yield': recipe_yield
            }

    def processing_content(self, content_xpaths):
        if type(content_xpaths) is not list:
            return content_xpaths.get() 
        contents = []
        for content_xpath in content_xpaths:
            item = content_xpath.get()
            contents.append(f'''{item}\n''')
        return "".join(contents)
    
    def processing_ingredient(self, ingredient_xpaths):
        #return ingredient_xpaths.get()
        ingredients = []
        for i in ingredient_xpaths:
            if i.xpath('text()'):
                name = i.xpath('text()').get().strip()
                ingredients.append(name)
        return "\n".join(ingredients)
    
    def processing_cooking_time(self, cooking_time):
        return re.findall(r'\d+' ,cooking_time)[0] if re.findall(r'\d+' ,cooking_time) else 'Estimate'
    
    def processing_recipe_yield(self,recipe_yield_xpaths):
        recipe_yields = []
        for i in recipe_yield_xpaths:
            number = i.xpath('p[1]/text()').get()
            tip = i.xpath('p[2]/text()').get()
            data = f"{number}) {tip}"
            recipe_yields.append(data)
        return "\n".join(recipe_yields)