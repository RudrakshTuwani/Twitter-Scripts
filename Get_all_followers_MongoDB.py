#!/usr/bin/env python

import tweepy
import time
import datetime
from pymongo import MongoClient

# Opens MongoDB Database
client = MongoClient()
db = client['Twitter']
followers = db['Followers']
followers_added = db['Followers_added']

# Read all old followers user ids into a set.
follower_ids = set()
for follower in followers.find():
    user_id = follower['id']
    follower_ids.add(user_id)

# Takes care of the necessary login information
consumer_key = ###############
consumer_secret = ###############
access_token = ###############
access_token_secret = ###############

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)  

if(api.verify_credentials):
    print 'We sucessfully logged in'
    print ''

account_id = api.get_user('insert user account handle here').id

# Get all followers
user = tweepy.Cursor(api.followers, id=account_id).items()
counter = 0
new_ids = []

while True:
    try:
        u = next(user)
        userinfo = u._json
        if userinfo['id'] not in follower_ids:
            followers.insert_one(userinfo)
            new_ids.append(userinfo['id'])
            counter += 1
        else:
            break
        
    except tweepy.TweepError:
        print 'Followers written :', counter 
        print 'Sleeping for 15 minutes'
        print ''
        time.sleep(15*60)
        continue
    except StopIteration:
        break

today = datetime.datetime.now()
today = today.strftime('%d/%m/%Y')
followers_added.insert_one({today:new_ids, 'count':counter})

print 'All the followers were recorded'
