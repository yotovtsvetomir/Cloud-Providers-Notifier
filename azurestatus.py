import feedparser
import json
from pymongo import MongoClient
import pytz
from dateutil.tz import tzutc, tzlocal
from datetime import datetime
import time


start = time.time()


#Get feed from corresponding api
feed = feedparser.parse('https://azure.microsoft.com/en-us/status/feed.atom')
#Organize data
for entry in feed.entries:
    print entry.id





end = time.time()
