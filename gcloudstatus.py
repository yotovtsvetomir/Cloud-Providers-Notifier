#!/usr/bin/env python
import feedparser
import json
from pymongo import MongoClient
import pytz
from dateutil.tz import tzutc, tzlocal
from datetime import datetime
import time


start = time.time()

#Connect DB
client = MongoClient()
db = client.gcloud
posts = db.posts


def canIadd(newID):
    c = posts.find({'_id': newID}).count()
    if c == 0:
        return True
    else:
        return False


#Get feed from corresponding api
feed = feedparser.parse('https://status.cloud.google.com/feed.atom')
#Organize data
for entry in feed.entries:
    if canIadd(entry.id) == True:
        data = {
        '_id' : entry.id,
        'published' : entry.date,
        'title' : entry.title,
        'summary': entry.summary
        }
        post_id =  posts.insert_one(data).inserted_id
    else:
        break

end = time.time()
