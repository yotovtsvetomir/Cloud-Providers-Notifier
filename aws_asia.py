#!/usr/bin/env python
import feedparser
import json
from pymongo import MongoClient
import pytz
from dateutil.tz import tzutc, tzlocal
from datetime import datetime
import time
import threading
from shortid import ShortId



#AWS services and servers for NA
services = ['apigateway-ap-south-1','apigateway-ap-northeast-2','apigateway-ap-southeast-1','apigateway-ap-southeast-2',
                  'apigateway-ap-northeast-1','appstream2-ap-northeast-1','athena-ap-southeast-1','athena-ap-northeast-1','chime',
                  'clouddirectory-ap-southeast-1','clouddirectory-ap-southeast-2','cloudfront','cloudsearch-ap-northeast-2',
                  'cloudsearch-ap-southeast-1','cloudsearch-ap-southeast-2','cloudsearch-ap-northeast-1','cloudwatch-ap-south-1',
                  'cloudwatch-ap-northeast-2','cloudwatch-ap-southeast-1','cloudwatch-ap-southeast-2','cloudwatch-ap-northeast-1',
                  'cognito-ap-south-1','cognito-ap-northeast-2','cognito-ap-southeast-2','cognito-ap-northeast-1','dynamodb-ap-south-1',
                  'dynamodb-ap-northeast-2','dynamodb-ap-southeast-1','dynamodb-ap-southeast-2','dynamodb-ap-northeast-1',
                  'dynamodb-dax-ap-northeast-1','ecr-ap-southeast-1','ecr-ap-southeast-2','ecr-ap-northeast-1','ecs-ap-southeast-1',
                  'ecs-ap-southeast-2','ecs-ap-northeast-1','ec2systemsmanager-ap-south-1','ec2systemsmanager-ap-northeast-2',
                  'ec2systemsmanager-ap-southeast-1','ec2systemsmanager-ap-southeast-2','ec2systemsmanager-ap-northeast-1',
                  'ec2-ap-south-1','ec2-ap-northeast-2','ec2-ap-southeast-1','ec2-ap-southeast-2','ec2-ap-northeast-1',
                  'elasticfilesystem-ap-southeast-2','elb-ap-south-1','elb-ap-northeast-2','elb-ap-southeast-1','elb-ap-southeast-2',
                  'elb-ap-northeast-1','emr-ap-south-1','emr-ap-northeast-2','emr-ap-southeast-1','emr-ap-southeast-2',
                  'emr-ap-northeast-1','elastictranscoder-ap-south-1','elastictranscoder-ap-southeast-1','elastictranscoder-ap-southeast-2',
                  'elastictranscoder-ap-northeast-1','elasticache-ap-south-1','elasticache-ap-northeast-2','elasticache-ap-southeast-1',
                  'elasticache-ap-southeast-2','elasticache-ap-northeast-1','elasticsearch-ap-south-1','elasticsearch-ap-northeast-2',
                  'elasticsearch-ap-southeast-1','elasticsearch-ap-southeast-2','elasticsearch-ap-northeast-1','gamelift-ap-south-1',
                  'gamelift-ap-northeast-2','gamelift-ap-southeast-1','gamelift-ap-northeast-1','glacier-ap-south-1','glacier-ap-northeast-2',
                  'glacier-ap-southeast-2','glacier-ap-northeast-1','inspector-ap-south-1','inspector-ap-northeast-2','inspector-ap-southeast-2',
                  'inspector-ap-northeast-1','kinesis-ap-south-1','kinesis-ap-northeast-2','kinesis-ap-southeast-1','kinesis-ap-southeast-2',
                  'kinesis-ap-northeast-1','lightsail-ap-south-1','lightsail-ap-southeast-1','lightsail-ap-southeast-2','lightsail-ap-northeast-1',
                  'redshift-ap-south-1','redshift-ap-northeast-2','redshift-ap-southeast-1','redshift-ap-southeast-2','redshift-ap-northeast-1',
                  'rds-ap-south-1','rds-ap-northeast-2','rds-ap-southeast-1','rds-ap-southeast-2','rds-ap-northeast-1','route53',
                  'route53domainregistration','route53-ap-south-1','route53-ap-northeast-2','route53-ap-southeast-1','route53-ap-southeast-2',
                  'route53-ap-northeast-1','sns-ap-south-1','sns-ap-northeast-2','sns-ap-southeast-1','sns-ap-southeast-2','sns-ap-northeast-1',
                  'sqs-ap-south-1','sqs-ap-northeast-2','sqs-ap-southeast-1','sqs-ap-southeast-2','sqs-ap-northeast-1','s3-ap-south-1',
                  's3-ap-northeast-2','s3-ap-southeast-1','s3-ap-southeast-2','s3-ap-northeast-1','swf-ap-south-1','swf-ap-northeast-2',
                  'swf-ap-southeast-1','swf-ap-southeast-2','swf-ap-northeast-1','simpledb-ap-southeast-1','simpledb-ap-southeast-2',
                  'simpledb-ap-northeast-1','vpc-ap-south-1','vpc-ap-northeast-2','vpc-ap-southeast-1','vpc-ap-southeast-2',
                  'vpc-ap-northeast-1','workdocs-ap-southeast-1','workdocs-ap-southeast-2','workdocs-ap-northeast-1',
                  'workspaces-ap-southeast-1','workspaces-ap-southeast-2','workspaces-ap-northeast-1','autoscaling-ap-south-1',
                  'autoscaling-ap-northeast-2','autoscaling-ap-southeast-1','autoscaling-ap-southeast-2','autoscaling-ap-northeast-1',
                  'batch-ap-northeast-1','certificatemanager-ap-south-1','certificatemanager-ap-northeast-2',
                  'certificatemanager-ap-southeast-1','certificatemanager-ap-southeast-2','certificatemanager-ap-northeast-1',
                  'cloudformation-ap-south-1','cloudformation-ap-northeast-2','cloudformation-ap-southeast-1',
                  'cloudformation-ap-southeast-2','cloudformation-ap-northeast-1','cloudhsm-ap-southeast-1','cloudhsm-ap-southeast-2',
                  'cloudhsm-ap-northeast-1','cloudtrail-ap-south-1','cloudtrail-ap-northeast-2','cloudtrail-ap-southeast-1',
                  'cloudtrail-ap-southeast-2','cloudtrail-ap-northeast-1','codebuild-ap-southeast-1','codebuild-ap-southeast-2',
                  'codebuild-ap-northeast-1','codecommit-ap-northeast-2','codecommit-ap-southeast-1','codecommit-ap-southeast-2',
                  'codecommit-ap-northeast-1','codedeploy-ap-south-1','codedeploy-ap-northeast-2','codedeploy-ap-southeast-1',
                  'codedeploy-ap-southeast-2','codedeploy-ap-northeast-1','codepipeline-ap-southeast-1','codepipeline-ap-southeast-2',
                  'codepipeline-ap-northeast-1','config-ap-south-1','config-ap-northeast-2','config-ap-southeast-1','config-ap-southeast-2',
                  'config-ap-northeast-1','datapipeline-ap-southeast-2','datapipeline-ap-northeast-1','dms-ap-south-1','dms-ap-northeast-2',
                  'dms-ap-southeast-1','dms-ap-southeast-2','dms-ap-northeast-1','directconnect-ap-south-1','directconnect-ap-northeast-2',
                  'directconnect-ap-southeast-1','directconnect-ap-southeast-2','directconnect-ap-northeast-1',
                  'directoryservice-ap-northeast-2','directoryservice-ap-southeast-1','directoryservice-ap-southeast-2',
                  'directoryservice-ap-northeast-1','elasticbeanstalk-ap-south-1','elasticbeanstalk-ap-northeast-2',
                  'elasticbeanstalk-ap-southeast-1','elasticbeanstalk-ap-southeast-2','elasticbeanstalk-ap-northeast-1','iam-ap-south-1',
                  'iam-ap-northeast-2','iam-ap-southeast-1','iam-ap-southeast-2','iam-ap-northeast-1','import-export',
                  'internetconnectivity-ap-south-1','internetconnectivity-ap-northeast-2','internetconnectivity-ap-southeast-1',
                  'internetconnectivity-ap-southeast-2','internetconnectivity-ap-northeast-1','awsiot-ap-northeast-2','awsiot-ap-southeast-1',
                  'awsiot-ap-southeast-2','awsiot-ap-northeast-1','kms-ap-south-1','kms-ap-northeast-2','kms-ap-southeast-1',
                  'kms-ap-southeast-2','kms-ap-northeast-1','lambda-ap-south-1','lambda-ap-northeast-2','lambda-ap-southeast-1',
                  'lambda-ap-southeast-2','lambda-ap-northeast-1','management-console','marketplace','opsworks-ap-south-1',
                  'opsworks-ap-northeast-2','opsworks-ap-southeast-1','opsworks-ap-southeast-2','opsworks-ap-northeast-1',
                  'organizations','resourcegroupstaggingapi-ap-south-1','resourcegroupstaggingapi-ap-northeast-2',
                  'resourcegroupstaggingapi-ap-southeast-1','resourcegroupstaggingapi-ap-southeast-2',
                  'resourcegroupstaggingapi-ap-northeast-1','servicecatalog-ap-southeast-1','servicecatalog-ap-southeast-2',
                  'servicecatalog-ap-northeast-1','state-ap-northeast-1','storagegateway-ap-south-1','storagegateway-ap-northeast-2',
                  'storagegateway-ap-southeast-1','storagegateway-ap-southeast-2','storagegateway-ap-northeast-1','awswaf',
                  'xray-ap-south-1','xray-ap-northeast-2','xray-ap-southeast-1','xray-ap-southeast-2','xray-ap-northeast-1']


#Connect/Create DB US EAST
client = MongoClient()
db = client.aws
asiaposts = db.asiaposts

#Check if exists in DB
def canIadd(newID):
    c = asiaposts.find({'_id': newID}).count()
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
                #Format datetime
                s1 = entry.published[:-3].strip()
                s2 = ttz.localize(datetime.strptime(s1, '%a, %d %b %Y %H:%M:%S'))
                data = {
                '_id' : entry.id + s,
                'published' : s2,
                'title' : entry.title,
                'summary': entry.summary
                }
                #Fill data if new
                post_id = asiaposts.insert_one(data).inserted_id
            else:
                break

    end = time.time()
    print "Updating time for Asia region: " + str(end - start)


def repeatt():
    updateDB()
    threading.Timer(2.0,repeatt).start()


if __name__ == "__main__":
        repeatt()
