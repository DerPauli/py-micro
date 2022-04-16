import os
import pymongo
import json
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
        for tweet in tweets:
            td = {
                "id": tweet['id'],
                "text": tweet['text'],
                "name": tweet['name'],
                "username": tweet['username'],
                "verified": tweet['verified'],
                "author_id": tweet['author_id'],
                "created_at": tweet['created_at'],
                "public_metrics": tweet['public_metrics'],
                "source": tweet['source']
            }

            self.collection.update_one(filter={'id': tweet['id']}, update={"$set": td}, upsert=True)

    def get_all_tweets(self, max_entries=0):
        r = []
        c = self.collection.find().limit(max_entries)
        
        for i in c:
            r.append(i)

        return r

    def print_bson(self, bson):
        print(json.dumps(json.loads(self.convert_to_json(bson)), indent=4, sort_keys=True))