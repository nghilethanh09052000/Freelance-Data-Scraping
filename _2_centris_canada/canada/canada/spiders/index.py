import scrapy
import json
from scrapy.selector import Selector

class IndexSpider(scrapy.Spider):
    name = 'index'
    allowed_domains = ['www.centris.ca']
    position = {
        "startPosition": 0
    }
    
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
            address = f'''{listing.xpath('normalize-space(.//div[@class="shell"]/a/div/div[3]/span[1]/div/text())').get()} - {listing.xpath('.//div[@class="shell"]/a/div/div[3]/span[2]/div[1]/text()').get()} - {listing.xpath('.//div[@class="shell"]/a/div/div[3]/span[2]/div[2]/text()').get()}'''
            detailUrl = listing.xpath('.//div[@class="shell"]/div/a/@href').get()
    
            yield {
                'Category': category,
                'Price': price,
                'ImageUrl': imageUrl,
                'Address': address,
                'Detail Url': detailUrl
            }

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
