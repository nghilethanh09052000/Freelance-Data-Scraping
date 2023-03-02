import scrapy
# from scrapy.pipelines.images import ImagesPipeline
import pymongo
from crawlmaster.settings import mongo_uri,db_name,collection,db_user,db_password
import os
# import gridfs
# from PIL import Image

class CustomUserIdPipeline(object):
    def __init__(self, settings=None):
        print('pipeline starting')
        if db_user:
            self.conn = pymongo.MongoClient(
            host=mongo_uri,
            ursername=db_user,
            password=db_password)
        else:   
            self.conn = pymongo.MongoClient(
            host=mongo_uri)
        db = self.conn[db_name]
        self.db = db
        self.collection = db[collection]

    def process_item(self, item, spider):
        print('inside item_complted')
        self.collection.insert_one(dict(item))
        return item