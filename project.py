# project.py

import os
import tweepy as tw
import spacy
import pandas as pd
import numpy as np
import requests
import json

CONSUMER_KEY = os.environ['TW_API_KEY']
CONSUMER_SECRET = os.environ['TW_API_SECRET_KEY']
BEARER_TOKEN = os.environ['TW_BEARER_TOKEN']
#auth = tw.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
#api = tw.API(auth, wait_on_rate_limit=True)


auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
#auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

search_words = "game of thrones"
date_since = "201904010000"
date_until = "202004010000"

#tweets = api.search_30_day(label='dev', query=search_words, fromDate=date_since, toDate=date_until, maxResults=5)

#tweets = (api.search_full_archive(label='dev', query=search_words, fromDate=date_since, toDate=date_until, maxResults=10))
#print(tweets[0])

""" 
with open('tweets.txt', 'w') as f:
    tweets = api.search_full_archive(label='dev', query=search_words, fromDate=date_since, toDate=date_until, maxResults=10)
    for t in tweets:
            f.write(t.text)
            #json.dump(t, outfile)
    for i in range(3):
        tweets = api.search_full_archive(label='dev', query=search_words, fromDate=date_since, toDate=date_until, maxResults=20)
        for t in tweets:
            f.write(t.text)
            #json.dump(t, outfile)
            #print(t.text, t.created_at)
 """


client = tw.Client(bearer_token=BEARER_TOKEN)

# Replace with your own search query
query = 'from:suhemparack -is:retweet'


#Para poder acceder a all tweet necesito academic research, si no, no me deja
#tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'], max_results=100)
# tweets = client.search_all_tweets(query=query, tweet_fields=['context_annotations', 'created_at'], max_results=100)


import re
def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

 # Replace with your own search query
#query = '(squid game) OR (juego calamar) OR (netflix calamar) (lang:es -is:retweet -has:media)'
query = 'juego calamar lang:es -(has:media) -is:retweet'
# Name and path of the file where you want the Tweets written to
file_name = 'tweets_squid.txt'

with open(file_name, 'a+') as f:
    for tweet in tw.Paginator(client.search_recent_tweets, query=query,
                                  tweet_fields=['context_annotations', 'created_at'], max_results=10).flatten(
            limit=10):
        text = remove_emoji(tweet.text.replace('\n',' '))
        data = {
            "text": text,
            "created_at": str(tweet.created_at),
            "id": tweet.id,
            "context_annotations": tweet.context_annotations,
        }
        json.dump(data, f)
        f.write("\n")
        #f.write(f"{tweet.text}\n{tweet.created_at}\n{tweet.id}\n{tweet.context_annotations}\n-\n")

#words = "infumable absurdo absurda mal malisimo pesimo horrible mala malita fea malisima gusta buena zarpada sarpada buenisima verla tremenda locura".split(' ')
#
#with open('data.txt') as json_file:
#    data = json.load(json_file)
#    