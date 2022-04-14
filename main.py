from net.client import Client
from db.db import MongoDB
from dotenv import load_dotenv

import json

baseUrl = 'https://api.twitter.com/2/'

def main():
    load_dotenv()

    c = Client(baseUrl)
    m = MongoDB()

    t = c.load_latest_tweets('Tesla')
    bson = m.attach_oids(t)

    #print(json.dumps(json.loads(m.convert_to_json(t)), indent=4, sort_keys=True))
    m.insert_tweets(bson)

if __name__ == "__main__":
    main()
