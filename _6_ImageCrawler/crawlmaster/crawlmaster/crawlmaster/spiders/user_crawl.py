import scrapy
import datetime
import requests
import json
# from scrapy.utils.response import open_in_browser
from crawlmaster.settings import flickr_url#, format,limit
# from crawlmaster.items import UserCrawlItem

class UserCrawlSpider(scrapy.Spider):
	name = 'user_crawl'
	
	def start_requests(self):
		# count = 0
		self.api_key = self.parse_apikey()
		done = set()
		i =1
		while True:
			if i == 5:#180
				break
			url_50_users = f'https://api.flickr.com/services/rest?username=pe&exact=0&extras=path_alias%2Crev_ignored%2Crev_contacts%2Cis_pro%2Cicon_urls%2Clocation%2Crev_contact_count%2Cuse_vespa%2Cdate_joined&per_page=50&page={i}&show_more=1&perPage=50&loadFullContact=1&isCollection=1&viewerNSID=&method=flickr.people.search&csrf=&api_key={self.api_key}&format=json&hermes=1&hermesClient=1&reqId=06656828-4cd5-4327-987b-13c1af34f492&nojsoncallback=1'
			response = json.loads(requests.get(url_50_users).text).get('people').get('person')
			urls = []
			print(response)
			for person in response:
				# print(person,'hereiam')
				if person.get('path_alias') == None:
					person_url = f'https://www.flickr.com/photos/{person.get("nsid")}'
				else:
					person_url = f'https://www.flickr.com/photos/{person.get("path_alias")}'
				item = {
					'nsid': person.get('nsid'),
					'path_alias': person.get('path_alias'),
					'is_pro': person.get('is_pro'),
					'url': person_url,
					'realname': person.get('realname'),
					'contact_count': person.get('rev_contact_count'),
					'username': person.get('username'),
					'date_joined': person.get('date_joined'),
					'public_photos_count': person.get('public_photos_count')}
				urls.append({'url': person_url, 'item': item})

			for url in urls:
				if url.get('url') in done:
					pass
				else:
					done.add(url.get('url'))
					yield scrapy.Request(url.get('url'), callback=self.parse_user, meta={'item':url.get('item')})
			i += 1
	def parse_apikey(self):
		response = requests.get(flickr_url).text
		return str(str(str(response).split('root.YUI_config.flickr.api.site_key = "')[1]).split('";')[0])
	def parse_user(self, response):
		print('entered parse')
		print(response.url)
		yield response.meta['item']

# TODO GO to login page copy CSRF and use it together with username and password to login
# visit a group and get the list of users.l
