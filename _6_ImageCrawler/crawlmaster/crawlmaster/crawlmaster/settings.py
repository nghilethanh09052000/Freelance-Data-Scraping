from configparser import ConfigParser

config = ConfigParser(interpolation=None)
config.read('crawler.cfg')

#[DATABASE]
mongo_uri = config['DATABASE']['mongo_uri']

if len(config['DATABASE']['db_user'])>0:
    db_user = config['DATABASE']['db_user']
else:
    db_user = None
if len(config['DATABASE']['db_password'])>0:
    db_password = config['DATABASE']['db_password']
else:
    db_password = None

db_name = config['DATABASE']['db_name']
collection = config['DATABASE']['collection']
metadata_path = config['DATABASE']['metadata_path']

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'crawlmaster.pipelines.CustomUserIdPipeline': 100,
}


BOT_NAME = 'crawlmaster'
SPIDER_MODULES = ['crawlmaster.spiders']
NEWSPIDER_MODULE = 'crawlmaster.spiders'
ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 10
DOWNLOAD_DELAY = 2

RETRY_ENABLED = False

flickr_message = (config['BOT']['flickr_message'])
flickr_url = (config['FLICKR']['flickr_url'])