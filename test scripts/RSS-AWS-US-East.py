#!/usr/bin/env python
import feedparser
import json
from pymongo import MongoClient
import pytz
from dateutil.tz import tzutc, tzlocal
from datetime import datetime


client = MongoClient()
db = client.aws
posts = db.posts

#Get feed from corresponding api
t = 'apigateway-us-east-1'
feed = feedparser.parse('http://status.aws.amazon.com/rss/%s.rss' % (t))
c = "empty"


tzz = pytz.timezone("US/Eastern")
#def toUTC(d):
#    return tzz.normalize(tzz.localize(d)).astimezone(pytz.utc)

#aware_datetime = toUTC(datetime.strptime(s1, '%a, %d %b %Y %H:%M:%S'))


#Organize data
for entry in feed.entries:
    s1 = entry.published[:-3].strip()
    s2 = tzz.localize(datetime.strptime(s1, '%a, %d %b %Y %H:%M:%S'))
    data = {
       '_id' : entry.id,
       'published' : s2,
       'title' : entry.title,
       'summary': entry.summary
    }
    #Check if post exists in the DB
    #cursor = posts.find({"_id": entry.id}).limit(50)
    cursor = posts.find({"_id": entry.id})
    for document in cursor:
        c = document
    if c == "empty":
        post_id = posts.insert_one(data).inserted_id

curs = posts.find()
for dat in curs:
    print dat
