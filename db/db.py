import os
import pymongo
from bson import json_util
from bson.objectid import ObjectId

class MongoDB():
    url = ''
    muri_key = 'MONGODB_URI'
    client = None

    default_db = 'local'
    default_coll = 'tweets'
    collection = None


    def __init__(self, url=None) -> None:
        if url != None:
            self.url = url
        else:
            self.url = os.getenv(self.muri_key)

        self.client = pymongo.MongoClient(self.url)
        self.collection = self.client[self.default_db][self.default_coll]

    def attach_oids(self, tweets):
        for tweet in tweets:
            tweet['_id'] = ObjectId()

        return tweets

    def convert_to_json(self, bson):
        return json_util.dumps(bson)

    def insert_tweets(self, tweets):
        self.collection.insert_many(tweets)