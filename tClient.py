import tweepy
import re
from tweepy import OAuthHandler


class tClient(object):

    def __init__(self):
        API_KEY = "API KEY HERE"
        API_SECRET = "API SECRET HERE"
        ACCESS_TOKEN = "ACCESS TOKEN HERE"
        ACCESS_TOKEN_SECRET = "ACCESS TOKEN SECRET HERE"

        try:
            self.auth = OAuthHandler(API_KEY, API_SECRET)
            self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def cleanTweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\ / \ / \S+)", " ", tweet).split())

    def get_tweets(self, query, count=10):
        tweets = []

        try:
            fetched_tweets = self.api.search_tweets(q=query, count=count)

            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(tweet.text)
                else:
                    tweets.append(tweet.text)
            return tweets

        except tweepy.TweepyException as e:
            print("Error : " + str(e))
