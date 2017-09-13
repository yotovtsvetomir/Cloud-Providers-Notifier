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
import checkchange

client = MongoClient()
db = client.aws_us_east
posts = db.posts


for ser in aws_na.services:
    if checkchange.checkSingle():
        print "UTC NOW: " + str(datetime.utcnow())
        print True
    else:
        print False
