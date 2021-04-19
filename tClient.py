import tweepy
import re
from tweepy import OAuthHandler


class tClient(object):

    def __init__(self):
        API_KEY = "wrkfGtlO8MNC48rmp3LCgfBTL"
        API_SECRET = "1heD6NmvUNIGb5z8Gq1DOQXsHJsZLP8Ght6G6wi5RuF2FwN6wd"
        ACCESS_TOKEN = "1335744879369052160-kQyoz9nD9UJJRSQqKL8XlNr8JWYemZ"
        ACCESS_TOKEN_SECRET = "DsqvQSdtnpUf3qsC93dgB0IOC1sO1bdUGba9aclSAhRxN"

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
            fetched_tweets = self.api.search(q=query, count=count)

            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(tweet.text)
                else:
                    tweets.append(tweet.text)
            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))
