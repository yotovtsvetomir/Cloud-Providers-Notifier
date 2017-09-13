#!/usr/bin/env python
import feedparser
import json
from pymongo import MongoClient
import pytz
from dateutil.tz import tzutc, tzlocal
from datetime import datetime
import time
import threading
import aws_na

client = MongoClient()
db = client.aws_us_east
posts = db.posts


def canIadd(newID):
    c = posts.find({'_id': newID}).count()
    if c == 0:
        return True
    else:
        return False

easttz = pytz.timezone("US/Eastern")
for serv in aws_na.services:
    print "Populating and Updating database - " + serv

    feed = feedparser.parse('http://status.aws.amazon.com/rss/%s.rss' % (serv))
    start = time.time()
    for entry in feed.entries:
        if  canIadd(entry.id) == True:
            s1 = entry.published[:-3].strip()
            s2 = easttz.localize(datetime.strptime(s1, '%a, %d %b %Y %H:%M:%S'))
            data = {
            '_id' : entry.id,
            'published' : s2,
            'title' : entry.title,
            'summary': entry.summary
            }
        else:
            s1 = entry.published[:-3].strip()
            s2 = easttz.localize(datetime.strptime(s1, '%a, %d %b %Y %H:%M:%S'))
            print str(s2)
            break
    end = time.time()
    print "time needed: " + str(end - start)
