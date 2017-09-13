#!/usr/bin/env python
import feedparser
import json
from pymongo import MongoClient
import pytz
from dateutil.tz import tzutc, tzlocal
from datetime import datetime
import time
import threading



#AWS services and servers for NA
services = ['apigateway-eu-central-1','apigateway-eu-west-1','apigateway-eu-west-2','appstream2-eu-west-1','athena-eu-west-1',
                  'chime','clouddirectory-eu-west-1','clouddirectory-eu-west-2','cloudfront','cloudsearch-eu-central-1','cloudsearch-eu-west-1',
                  'cloudwatch-eu-central-1','cloudwatch-eu-west-1','cloudwatch-eu-west-2','cognito-eu-central-1','cognito-eu-west-1',
                  'cognito-eu-west-2','dynamodb-eu-central-1','dynamodb-eu-west-1','dynamodb-eu-west-2','dynamodb-dax-eu-west-1',
                  'ecr-eu-central-1','ecr-eu-west-1','ecr-eu-west-2','ecs-eu-central-1','ecs-eu-west-1','ecs-eu-west-2',
                  'ec2systemsmanager-eu-central-1','ec2systemsmanager-eu-west-1','ec2systemsmanager-eu-west-2','ec2-eu-central-1',
                  'ec2-eu-west-1','ec2-eu-west-2','elasticfilesystem-eu-west-1','elb-eu-central-1','elb-eu-west-1','elb-eu-west-2','emr-eu-central-1',
                  'emr-eu-west-1','emr-eu-west-2','elastictranscoder-eu-west-1','elasticache-eu-central-1','elasticache-eu-west-1',
                  'elasticache-eu-west-2','elasticsearch-eu-central-1','elasticsearch-eu-west-1','elasticsearch-eu-west-2','gamelift-eu-central-1',
                  'gamelift-eu-west-1','glacier-eu-central-1','glacier-eu-west-1','glacier-eu-west-2','inspector-eu-west-1','kinesis-eu-central-1',
                  'kinesis-eu-west-1','kinesis-eu-west-2','kinesisanalytics-eu-west-1','firehose-eu-west-1','lightsail-eu-central-1','lightsail-eu-west-1',
                  'lightsail-eu-west-2','aml-eu-west-1','polly-eu-west-1','redshift-eu-central-1','redshift-eu-west-1','redshift-eu-west-2',
                  'rekognition-eu-west-1','rds-eu-central-1','rds-eu-west-1','rds-eu-west-2','route53','route53domainregistration',
                  'route53-eu-central-1','route53-eu-west-1','route53-eu-west-2','ses-eu-west-1','sns-eu-central-1','sns-eu-west-1',
                  'sns-eu-west-2','sqs-eu-central-1','sqs-eu-west-1','sqs-eu-west-2','s3-eu-central-1','s3-eu-west-1','s3-eu-west-2',
                  'swf-eu-central-1','swf-eu-west-1','swf-eu-west-2','simpledb-eu-west-1','vpc-eu-central-1','vpc-eu-west-1',
                  'vpc-eu-west-2','workdocs-eu-west-1','workmail-eu-west-1','workspaces-eu-central-1','workspaces-eu-west-1',
                  'autoscaling-eu-central-1','autoscaling-eu-west-1','autoscaling-eu-west-2','batch-eu-west-1','certificatemanager-eu-central-1',
                  'certificatemanager-eu-west-1','certificatemanager-eu-west-2','cloudformation-eu-central-1','cloudformation-eu-west-1',
                  'cloudformation-eu-west-2','cloudhsm-eu-central-1','cloudhsm-eu-west-1','cloudtrail-eu-central-1','cloudtrail-eu-west-1',
                  'cloudtrail-eu-west-2','codebuild-eu-central-1','codebuild-eu-west-1','codecommit-eu-central-1','codecommit-eu-west-1',
                  'codecommit-eu-west-2','codedeploy-eu-central-1','codedeploy-eu-west-1','codedeploy-eu-west-2','codepipeline-eu-central-1',
                  'codepipeline-eu-west-1','codestar-eu-west-1','config-eu-central-1','config-eu-west-1','config-eu-west-2','datapipeline-eu-west-1',
                  'dms-eu-central-1','dms-eu-west-1','dms-eu-west-2','directconnect-eu-central-1','directconnect-eu-west-1',
                  'directconnect-eu-west-2','directoryservice-eu-central-1','directoryservice-eu-west-1','directoryservice-eu-west-2',
                  'elasticbeanstalk-eu-central-1','elasticbeanstalk-eu-west-1','elasticbeanstalk-eu-west-2','iam-eu-central-1','iam-eu-west-1',
                  'iam-eu-west-2','import-export','internetconnectivity-eu-central-1','internetconnectivity-eu-west-1',
                  'internetconnectivity-eu-west-2','awsiot-eu-central-1','awsiot-eu-west-1','awsiot-eu-west-2','kms-eu-central-1','kms-eu-west-1',
                  'kms-eu-west-2','lambda-eu-central-1','lambda-eu-west-1','lambda-eu-west-2','management-console','marketplace',
                  'opsworkschef-eu-west-1','opsworks-eu-central-1','opsworks-eu-west-1','opsworks-eu-west-2','organizations',
                  'quicksight-eu-west-1','resourcegroupstaggingapi-eu-central-1','resourcegroupstaggingapi-eu-west-1',
                  'resourcegroupstaggingapi-eu-west-2','servicecatalog-eu-central-1','servicecatalog-eu-west-1','servicecatalog-eu-west-2',
                  'state-eu-central-1','state-eu-west-1','storagegateway-eu-central-1','storagegateway-eu-west-1','storagegateway-eu-west-2',
                  'awswaf','xray-eu-central-1','xray-eu-west-1','xray-eu-west-2',]


#Connect DB - EU
client = MongoClient()
db = client.aws
euposts = db.euposts

#Check if exists in DB
def canIadd(newID):
    c = euposts.find({'_id': newID}).count()
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
                post_id = euposts.insert_one(data).inserted_id
            else:
                break

    end = time.time()
    print "Updating time for EU region: " + str(end - start)


def repeatt():
    updateDB()
    threading.Timer(2.0,repeatt).start()


if __name__ == "__main__":
        repeatt()
