import os
import requests

class Client:
    tt_key = 'TWITTER_TOKEN'
    url = 'default.com'
    default_headers = {
        'Content-type': 'application/json'
    }

    def __init__(self, url) -> None:
        self.url = url


    def __add_headers(self, default_headers: bool, headers: dict[str, str]) -> dict[str, str]:
        h = {}

        if default_headers:
            h = {**self.default_headers, **headers}

        return h

    def load_latest_tweets(self, from_user):
        # prepare bearer
        token = os.getenv(self.tt_key)

        if token == None:
            print("Panic: no Twitter token set")
            exit(-1)

        h = { 'Authorization': f'Bearer {token}' }

        if from_user != '':
            query_url = f'tweets/search/recent?query=from:{from_user}&tweet.fields=created_at,public_metrics,source&expansions=author_id&user.fields=created_at'
            r = requests.get(self.url + query_url, headers=self.__add_headers(True, h))
            
            if r != None:
                return r.json()['data']