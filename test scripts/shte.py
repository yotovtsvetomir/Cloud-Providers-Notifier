#!/usr/bin/env python
import feedparser
import json
from pymongo import MongoClient
import pytz
from dateutil.tz import tzutc, tzlocal
from datetime import datetime
import time
import threading

client = MongoClient()
aws = client.aws
naposts = aws.naposts
euposts = aws.euposts
saposts = aws.saposts
asiaposts = aws.asiaposts

def getAwsAll():
    output = []

    #NA posts
    for na in naposts.find().sort('published', -1):
            output.append(na)

    #Eurpoe Posts
    for eu in euposts.find().sort('published', -1):
            output.append(eu)

    #SA Posts
    for sa in saposts.find().sort('published', -1):
            output.append(sa)

    #Asia Posts
    for asi in asiaposts.find().sort('published', -1):
            output.append(asi)

    return output


def getByRegionAndService(region,service):
    output = []
    if region == "na":
        #NA posts
        for na in naposts.find().sort('published', -1):
            word = na['_id']
            if service in word:
               output.append(na)
    elif region == "eu":
        for eu in euposts.find().sort('published', -1):
                word = eu['_id']
                if service in word:
                  output.append(eu)
    elif region == "sa":
        for sa in saposts.find().sort('published', -1):
                word = sa['_id']
                if service in word:
                  output.append(sa)
    elif region == "asia":
        for asi in asiaposts.find().sort('published', -1):
                word = asi['_id']
                if service in word:
                  output.append(asi)

    if len(output) < 1:
        return "Please make sure that the service exists for the corresponding region if it does then probably there were no issues EVER. :)"
    else:
        return output
