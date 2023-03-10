import scrapy
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

    init_url = 'https://www.gutekueche.at'
    recipe_route = 'rezeptkategorien'
    all_recipe_route = 'alle-rezepte'


    def start_requests(self):
        yield SplashRequest(
            url = f"{self.init_url}/{self.recipe_route}",
            callback = self.find_category,
            splash_headers={'Authorization':basic_auth_header('user','userpass')},
        )
    
    def find_category(self, response):
        sections = response.xpath('//main/section[2]/section')
        for section in sections:
            topic = section.xpath('./h2/text()').get()
            recipe_list = section.xpath('./div[@class="quicklinks-grid quicklinks"]/ul/li/a/@href')
            for recipe in recipe_list:

                # init_url = https://www.gutekueche.at
                # recipe.get() = /antipasti-rezepte
                # all_recipe_route = alle-rezepte

                recipe_url = f'{self.init_url}{recipe.get().split("-")[0]}-{self.all_recipe_route}'

                yield SplashRequest(
                    url = recipe_url,
                    callback = self.list_recipe,
                    splash_headers={'Authorization':basic_auth_header('user','userpass')},
                    meta =  {
                        'url': recipe_url,
                        'topic': topic
                    }
                )

    def list_recipe(self, response):
        list_recipe = response.xpath('//div[@class="col "]')
        for recipe in list_recipe:
            url = recipe.xpath('.//div/div/div[2]/h3/a/@href').get()
            yield SplashRequest(
                url = f"{self.init_url}{url}",
                callback = self.init_recipe,
                splash_headers={'Authorization':basic_auth_header('user','userpass')},
                meta = {
                    'topic': response.meta['topic']
                } 
            )

        next_page = response.xpath("//li[contains(@class,'arrow')][last()]/a/@href").get()
        if next_page:
            recipe_url = f"{self.init_url}{next_page}"
            yield SplashRequest(
                    url = recipe_url,
                    callback = self.list_recipe,
                    splash_headers={'Authorization':basic_auth_header('user','userpass')},
                    meta =  {
                        'topic': response.meta['topic']
                    } 
                )
    
    def init_recipe(self, response):
        image_url = self.process_image( response.xpath('//main[@id="main"]/article/header')) 
        name = self.process_name( response.xpath('//main[@id="main"]/article/h1/text()').get() )
        summary = self.process_summary( response.xpath('//main[@id="main"]/article/div/p/text()').get() )    
        servings = self.process_servings(response.xpath('//span[@class="portions-group w100p"]/input/@value'))
        prep_time = self.process_prep_time(response.xpath('//p[@class="recipe-times"]/span/text()'))
        cook_time = self.process_cook_time(response.xpath('//p[@class="recipe-times"]/span/text()'))
        total_time = self.process_total_time(response.xpath('//p[@class="recipe-times"]/span/text()'))
        equipment = self.process_equipments( response.xpath('//div[@class="recipe-categories"]/span[contains(@class,"btn")]/text()')  )
        ingredients_flat = self.process_ingredients( response.xpath('//div[@class="ingredients-table"]/table') )
        instructions_flat = self.process_instructions( response.xpath('//section[@class="sec rezept-preperation"]/ol/li/text()') )
        video_embed = self.process_video_embed( response.xpath('//div[@type="video/mp4"]/video/@src') )
        notes = self.process_notes( response.xpath('//section[@class="sec"]/p/text()') )
        nutrition = self.process_nutrition( response.xpath('//div[@class="text-center"]/div[@class="nutri-block"]') )
        categories = self.process_categories( response.xpath('//div[@class="recipe-categories"]/a/text()') )

        yield {
            'url': response.url,
            'topic': response.meta['topic'],
            'categories': categories,   

            'type': 'food',
            'image_url': image_url,
            'pin_image_url': '', 
            'name': name,
            'summary': summary,
            "author_display": "disabled",
            "author_name": "",
            "author_link": "",
            "cost": "",
            "servings": servings,
            "servings_unit": "people",
            "prep_time": prep_time,
            "prep_time_zero": "",
            "cook_time": cook_time,
            "cook_time_zero": "",
            "total_time": total_time,
            "custom_time": "",
            "custom_time_zero": "",
            "custom_time_label": "Resting Time",
            "tags": {
                "course": [],
                "cuisine": [],
                "keyword": [],
                "difficulty": []
            },
            'equipment': equipment,
            'ingredients_flat': ingredients_flat,
            'instructions_flat': instructions_flat,
            "video_embed": video_embed,
            'notes': notes,
            'nutrition': nutrition,
            "custom_fields": {},
            "ingredient_links_type": "global",
        }

    def process_image(self, image_xpath):
        if image_xpath.xpath('.//picture/img/@src'):
            return image_xpath.xpath('.//picture/img/@src').get()
        return image_xpath.xpath('.//div/div/ul[1]/li/div/picture/img/@src').getall()

    def process_name(self, name):
        return name # string
    
    def process_summary(self, summary):
        return f'<p>{summary}</p>' # string
    
    def process_servings(self, servings):
        return servings.get() #Number
    
    def process_prep_time(self, prep_time):
        for row in prep_time:
            key =  row.get().split(".")[1].strip()
            value = row.get().split(".")[0]  
            if key == 'Zubereitungszeit': 
                return re.findall(r'\d+',value)[0] # string
        return ''
    
    def process_cook_time(self, cook_time):
        for row in cook_time:
            key =  row.get().split(".")[1].strip()
            value = row.get().split(".")[0]  
            if key == 'Koch & Ruhezeit': return re.findall(r'\d+',value)[0] # string
        return '' 
    
    def process_total_time(self, total_time):
        for row in total_time:
            key =  row.get().split(".")[1].strip()
            value = row.get().split(".")[0]  
            if key == 'Gesamtzeit': return re.findall(r'\d+',value)[0] # string
        return ''
    
    def process_equipments(self, equipments):
        data = []
        for equipment in equipments.getall():
            data.append({'name':equipment})
        return data
   
    def process_ingredients(self, ingredients):
        ingredients_list = []
        for ingredient in ingredients.xpath('.//tr'):       
            amount = ingredient.xpath('normalize-space(.//td/text())').get()
            unit = ingredient.xpath('normalize-space(.//th[1]/text())').get()
            name = ingredient.xpath('normalize-space(.//th[2]/a/text())').get() if ingredient.xpath('normalize-space(.//th[2]/a/text())').get() else ingredient.xpath('normalize-space(.//th[2]/text())').get()
            ingredients_list.append({
                'amount': amount,
                'unit': unit,
                'name': name,
                'notes': '',
                "converted": {},
                'type': 'ingredient'
            })
        return ingredients_list # Array Object
    
    def process_instructions(self, instructions):
        steps = []
        for index, instruction in enumerate(instructions.getall()):
            steps.append({
                'text': f'<p>{instruction}</p>',
                'type': 'instruction',
                'image_url': ""
            })
        return steps # Array Object
    
    def process_video_embed(self, video_embed):
        return video_embed.get() if video_embed.get() else ''
    
    def process_notes(self, notes):
        return f'<p>{notes.get()}</p>' if notes.get() else ''
    
    def process_nutrition(self, nutritions):
        data = {} 
        for nutrition in nutritions:
            key = nutrition.xpath('header/text()').get()
            if key == 'kcal':
                key = 'calories'
            elif key == 'Fett':
               key = 'fat'
            elif key == 'Eiweiß':
                key = 'protein'
            elif key == 'Kohlenhydrate':
                key = 'carbohydrates'

            value = nutrition.xpath('div/text()').get()
            value = re.findall("\d+(?:,\d+)?", value)[0]
            value = float(value.replace(",", ".")) if "," in value else int(value)

            data = {**data, key: value }

        return data

    def process_categories(self, categories):
        return categories.getall() # Array

   
    


   