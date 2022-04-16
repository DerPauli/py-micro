from curses import has_key
import os
import json
from textwrap import indent
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
            query_url = f'tweets/search/recent?query=from:{from_user}&tweet.fields=created_at,public_metrics,source&expansions=author_id&user.fields=created_at,name,username,verified'
            r = requests.get(self.url + query_url, headers=self.__add_headers(True, h))
            
            if r.status_code == r.ok:
                result_count = r.json().get('meta').get('result_count')
                if result_count > 0:
                    json = r.json().get('data')
                    for key in json:
                        key['name'] = r.json()['includes']['users'][0]['name']
                        key['username'] = r.json()['includes']['users'][0]['username']
                        key['verified'] = r.json()['includes']['users'][0]['verified']

                    return json
            
            return None