import scrapy
import json
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from w3lib.http import basic_auth_header

class IndexSpider(scrapy.Spider):
    name = 'index'
    allowed_domains = ['www.centris.ca']
    position = {
        "startPosition": 0
    }

    http_user = 'user'
    http_pass = 'userpass'

    lua_script = '''
        function main(splash, args)
            splash.images_enabled = false
            splash.js_enabled = false
            assert(splash:go(args.url))
            assert(splash:wait(0.5))
            return {
                html = splash:html()
            }
        end
    '''
    
    def start_requests(self):
        query = {
        "query": {
            "UseGeographyShapes": 0,
            "Filters": [
            {
                "MatchType": "CityDistrictAll",
                "Text": "Montréal (All boroughs)",
                "Id": 5
            }
            ],
            "FieldsValues": [
            {
                "fieldId": "CityDistrictAll",
                "value": 5,
                "fieldConditionId": "",
                "valueConditionId": ""
            },
            {
                "fieldId": "Category",
                "value": "Commercial",
                "fieldConditionId": "",
                "valueConditionId": ""
            },
            {
                "fieldId": "SellingType",
                "value": "Rent",
                "fieldConditionId": "",
                "valueConditionId": ""
            },
            {
                "fieldId": "RentPrice",
                "value": 0,
                "fieldConditionId": "ForRent",
                "valueConditionId": ""
            },
            {
                "fieldId": "RentPrice",
                "value": 3500,
                "fieldConditionId": "ForRent",
                "valueConditionId": ""
            }
            ]
        },
        "isHomePage": True
        }
        yield scrapy.Request(
            url = "https://www.centris.ca/property/UpdateQuery",
            method = "POST",
            body = json.dumps(query),
            headers = {
                'Content-Type': 'application/json'
            },
            callback = self.update_query
        )
        
    def update_query(self,response):
        yield scrapy.Request(
            url = "https://www.centris.ca/Property/GetInscriptions",
            method = "POST",
            body = json.dumps(self.position),
             headers = {
                'Content-Type': 'application/json'
            },
            callback = self.parse
        )

    def parse(self, response):

        resp_dict = json.loads(response.body)
        html = resp_dict.get('d').get('Result').get('html')

      
        sel = Selector(text = html)
        listings = sel.xpath('//div[@class="property-thumbnail-item thumbnailItem col-12 col-sm-6 col-md-4 col-lg-3"]')
        for listing in listings:
            category = listing.xpath('.//div[@class="shell"]/a/div/div[4]/div/div/span/text()').get()
            price = listing.xpath('.//div[@class="shell"]/a/div/div[2]/span[1]/text()').get()
            imageUrl = listing.xpath('.//div[@class="shell"]/div/a/img/@src').get()
            detailUrl = f'''https://www.centris.ca{listing.xpath('.//div[@class="shell"]/div/a/@href').get()}'''
    
          
            yield SplashRequest(
                url = detailUrl,
                endpoint='execute',
                callback=self.parse_summary,
                args={
                    'lua_source':self.lua_script
                },
                splash_headers={'Authorization':basic_auth_header('user','userpass')},
                meta= {
                    'Category': category,
                    'Price': price,
                    'ImageUrl': imageUrl,
                    'Detail Url': detailUrl
                }
            )

        count = resp_dict.get('d').get('Result').get('count')
        increment_number = resp_dict.get('d').get('Result').get('inscNumberPerPage')
        if self.position['startPosition'] <= count:
            self.position['startPosition'] += increment_number
        yield scrapy.Request(
            url = "https://www.centris.ca/Property/GetInscriptions",
            method = "POST",
            body = json.dumps(self.position),
             headers = {
                'Content-Type': 'application/json'
            },
            callback = self.parse
        )

    def parse_summary(self, response):
        category = response.request.meta['Category']
        price = response.request.meta['Price']
        imageUrl = response.request.meta['ImageUrl']
        detailUrl = response.request.meta['Detail Url']

        address = response.xpath('//div[@class="row property-tagline"]/div/div/div/h2/text()').get()
        description = response.xpath('normalize-space(//div[@itemprop="description"]/text())').get()
        
        yield {
            'Category': category,
            'Price': price,
            'ImageUrl': imageUrl,
            'Address': address,
            'Description': description,
            'Detail Url': detailUrl
        }

