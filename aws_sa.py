#!/usr/bin/env python
import feedparser
import json
from pymongo import MongoClient
import pytz
from dateutil.tz import tzutc, tzlocal
from datetime import datetime
import time
import threading


#AWS services and servers for SA
services = ['chime','cloudfront','cloudsearch-sa-east-1','cloudwatch-sa-east-1','dynamodb-sa-east-1',
                  'ec2systemsmanager-sa-east-1','ec2-sa-east-1','elb-sa-east-1','emr-sa-east-1','elasticache-sa-east-1',
                  'elasticsearch-sa-east-1','gamelift-sa-east-1','kinesis-sa-east-1','redshift-sa-east-1','rds-sa-east-1','route53',
                  'route53domainregistration','route53-sa-east-1','sns-sa-east-1','sqs-sa-east-1','s3-sa-east-1','swf-sa-east-1',
                  'simpledb-sa-east-1','vpc-sa-east-1','autoscaling-sa-east-1','certificatemanager-sa-east-1','cloudformation-sa-east-1',
                  'cloudtrail-sa-east-1','codecommit-sa-east-1','codedeploy-sa-east-1','codepipeline-sa-east-1','config-sa-east-1',
                  'dms-sa-east-1','directconnect-sa-east-1','elasticbeanstalk-sa-east-1','iam-sa-east-1','internetconnectivity-sa-east-1',
                  'kms-sa-east-1','lambda-sa-east-1','management-console','marketplace','opsworks-sa-east-1','organizations',
                  'resourcegroupstaggingapi-sa-east-1','storagegateway-sa-east-1','awswaf','xray-sa-east-1',]


#Connect  DB SA
client = MongoClient()
db = client.aws
saposts = db.saposts

#Check if exists in DB
def canIadd(newID):
    c = saposts.find({'_id': newID}).count()
    if c == 0:
        return True
    else:
        return False

def  updateDB():
    start = time.time()
    ttz = pytz.timezone("US/Pacific")

    #Get feed from corresponding api
    for serv in services:
        print "Populating and Updating database - " + serv
        feed = feedparser.parse('http://status.aws.amazon.com/rss/%s.rss' % (serv))
        #Organize data
        for entry in feed.entries:
            if canIadd(entry.id) == True:
                s1 = entry.published[:-3].strip()
                s2 = ttz.localize(datetime.strptime(s1, '%a, %d %b %Y %H:%M:%S'))
                data = {
                '_id' : entry.id,
                'published' : s2,
                'title' : entry.title,
                'summary': entry.summary
                }
                #Fill data if new
                post_id = saposts.insert_one(data).inserted_id
            else:
                break

    end = time.time()
    print "Updating time for SA region: " + str(end - start)




def repeatt():
    updateDB()
    threading.Timer(2.0,repeatt).start()


if __name__ == "__main__":
        repeatt()
