#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tweepy


CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_SECRET = os.environ['ACCESS_SECRET']
TARGET_ID = os.environ['TARGET_ID']


def get_api():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api


class ExStatus(tweepy.Status):
    def __init__(self, status):
        self.__dict__.update(status.__dict__)
        self.full_text = self._full_text()
        self.is_arcade = self._is_arcade(self.full_text)
        self.url = self._get_status_url()
    
    def _get_status_url(self):
        name = self.author.screen_name
        id_ = self.id_str
        url = f'https://twitter.com/{name}/status/{id_}'
        return url

    def _full_text(self):
        if hasattr(self, 'extended_tweet'):
            return self.extended_tweet['full_text']
        elif not hasattr(self, 'full_text'):
            return self.text
        else:
            return self.full_tex

    def _is_arcade(self, text):
        kw = '【カルデアアーケード広報局より】'
        return kw in self.full_text


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status_ori):
        status = ExStatus(status_ori)
        if status.author.id_str == TARGET_ID and not status.is_arcade:
            status.retweet()
            self.api.update_status(status.url)



def main():
    api = get_api()
    listener = MyStreamListener(api)
    stream = tweepy.Stream(auth=api.auth, listener=listener)
    stream.filter(follow=[TARGET_ID])


if __name__ == '__main__':
    main()
