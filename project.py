# project.py

import os
import tweepy as tw
import spacy
import pandas as pd
import numpy as np
import requests
import json
import unicodedata

CONSUMER_KEY = os.environ['TW_API_KEY']
CONSUMER_SECRET = os.environ['TW_API_SECRET_KEY']
BEARER_TOKEN = os.environ['TW_BEARER_TOKEN']

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

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def extract_tweets(input_file, output_file):
    with open(output_file, 'a+') as f:
        r = open(input_file, "r")
        Lines = r.readlines()
        count = 0
        for line in Lines:
            count += 1
            data = json.loads(line)
            f.write(remove_emoji(remove_accents(data['text']))+"\n")
    open(input_file, 'w').close()

def pass_tweets(input_file, output_file='tweets.txt'):
    with open(input_file, 'r+') as f:
        fileoutput = f.readlines()
        f.truncate(0)
    with open(output_file, "a+") as f1:
        for line in fileoutput:
            f1.write(line)
            f1.flush()


# context_annotatios tienen la forma: (como se repiten no lo voy a tomar)
# "context_annotations": [{"domain": {"id": "3", "name": "TV Shows",
# "description": "Television shows from around the world"},
# "entity": {"id": "1437413779755597824", "name": "Squid Game"}}]}

auth = tw.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tw.API(auth, wait_on_rate_limit=True)

def get_old_tweets(query, file_name, since, until, limit=1000):
    with open(file_name, 'a+') as f:
        for t in tw.Cursor(api.search_full_archive, label='dev', query=query, fromDate=since, toDate=until, maxResults=1000).items(limit):
            text = remove_emoji(remove_accents(t.text.replace('\n',' ')))
            data = {
                "text": text,
                "created_at": str(t.created_at),
                "id": t.id,
            }
            json.dump(data, f)
            f.write("\n")

query = '-(RT) juego calamar lang:es -(has:media)'
date_since = "202101010000"
date_until = "202110150000"
file_name = "old_tweets.txt"

#get_old_tweets(query, file_name, date_since, date_until, limit=10000)
#extract_tweets(file_name,"old_tweets_new.txt")
#pass_tweets("old_tweets_new.txt", "old_tweets.txt")


# ------------------------------------------------------------------------------------------

auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tw.API(auth, wait_on_rate_limit=True)
client = tw.Client(bearer_token=BEARER_TOKEN)


# Buscar con Hashtags 
query = 'juego calamar lang:es -(has:media) -is:retweet'
file_name = 'tweets_squid2.txt'

def get_tweets(query, file_name, limit=10):
    with open(file_name, 'a+') as f:
        for tweet in tw.Paginator(client.search_recent_tweets, query=query,
                                    tweet_fields=['created_at'], max_results=100).flatten(
                limit=limit):
            text = remove_emoji(remove_accents(tweet.text.replace('\n',' ')))
            data = {
                "text": text,
                "created_at": str(tweet.created_at),
                "id": tweet.id,
            }
            json.dump(data, f)
            f.write("\n")


get_tweets(query, file_name, limit=1000)
extract_tweets(file_name,"tweets_new.txt")
pass_tweets("tweets_new.txt")