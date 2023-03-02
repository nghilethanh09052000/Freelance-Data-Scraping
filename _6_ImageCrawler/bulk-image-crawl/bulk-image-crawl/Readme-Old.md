# Scrapping_Img

1. Install python 3.10
2. pip install scrapy scrapy-splash Pillow pymongo requests\
\
Settings: \
\
flickr_url : paste here url\
flickr_api_key : paste here api key\
limit = 4000 : at flickr limit 4000 per tag now so it is not works\
IMAGES_STORE : directory where save img and resize img\
IMAGES_THUMBS : resizing by scrapy\
mongo_uri : url to mongo db\
db_user = None ( if no user/pass in db ) and db_user = 'username' ( when in db is user/pass )\
gridfs : If False dont save img to mongo db. If True saves\
root_class and sub_class used in scrappind\
CONCURRENT_REQUESTS = 100 ( How many one time will do tasks )\
\
Start crawling:\
scrapy crawl flickr ( without saving json )\
scrapy crawl flickr -O result.json ( with saving json )
