import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from img.spiders.flickr import ImgSpider


process = CrawlerProcess(settings=get_project_settings())
process.crawl(ImgSpider)
process.start()