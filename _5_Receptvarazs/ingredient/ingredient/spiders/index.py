import scrapy
import json
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from w3lib.http import basic_auth_header

from ..recipe_url import recipe_urls
from ..category_url import category_url

class IndexSpider(scrapy.Spider):
    http_user = 'user'
    http_pass = 'userpass'
    init_url = 'https://web.archive.org/web/20220517171055/'
    error_urls = []
    name = 'index'
    allowed_domains = ['web.archive.org']

    def start_requests(self):
        for recipe_url in recipe_urls:
            yield SplashRequest(
                url = f'''{self.init_url}{recipe_url}''',
                callback = self.parse,
                splash_headers={'Authorization':basic_auth_header('user','userpass')},
                meta = {
                    'recipe_url': recipe_url
                }
            )

    def parse(self, response):

        recipe_category = self.processing_recipe_category(response.xpath('normalize-space(//div[@class="breadcrumb"]/a[3]/text())'))   
        
        recipe_title = self.processing_recipe_title(response.xpath('normalize-space(//div[@class="item"]/h1/text())'))
        recipe_picture = self.processing_recipe_picture(response.xpath('//td[@class="item_image"]/div/a/img/@src'))
        recipe_intro = self.processing_recipe_intro(response.xpath('normalize-space(//div[@class="lead"]/p/text())'))
        servings = self.processing_servings(response.xpath('//input[@id="parameter_hanyszemelyre"]/@value'))
        ingredients = self.processing_ingredients(response.xpath('//div[@class="ingredients"]/ul[@class="ingredients_list"]/li'))
        direction_recipe = self.processing_direction_recipe(response.xpath('//div[@class="steps"]/p'))

        yield {
            'Recipe_Url': response.meta['recipe_url'],
            'Recipe Category': recipe_category,
            'Recipe Title': recipe_title, 
            'Recipe Picture': recipe_picture,
            'Recipe Intro': recipe_intro, 
            'Servings': servings,
            'Ingredients': ingredients,
            'Direction/Recipe': direction_recipe
        }

    def processing_recipe_category(self, recipe_category_xpath):
        return recipe_category_xpath.get()
    
    def processing_recipe_title(self, recipe_title_xpath):
        return recipe_title_xpath.get()

    def processing_recipe_picture(self, recipe_picture_xpath):
        return recipe_picture_xpath.get()

    def processing_recipe_intro(self, recipe_intro_xpath):
        return recipe_intro_xpath.get()
    
    def processing_servings(self, servings_xpath):
        return servings_xpath.get()
    
    def processing_ingredients(self, ingredients_xpath):
        ingredients = []

        for ingredient_xpath in ingredients_xpath:
            ingredient_amount = ingredient_xpath.xpath('span[@class="adjustable"]/@data-amount').get(default=None)
            ingredient_name = ingredient_xpath.xpath('text()').get().strip()
            if ingredient_amount:
                ingredient = f'''{ingredient_amount} {ingredient_name}'''
            else:
                ingredient = ingredient_name
            ingredients.append(ingredient)

        return "\n".join(ingredients)

    def processing_direction_recipe(self, direction_recipe_xpath):
        steps = []
        for step in direction_recipe_xpath: 
            item = step.xpath('.//text()').get()
            steps.append(f'''{item}\n''')
        return "".join(steps)


