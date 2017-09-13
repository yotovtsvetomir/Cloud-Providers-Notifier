#!/usr/bin/env python
import feedparser
import json
from pymongo import MongoClient
import pytz
from dateutil.tz import tzutc, tzlocal
from datetime import datetime
import time


start = time.time()

#AWS services and servers for NA
services = [
          'apigateway-us-west-1','apigateway-us-east-1','apigateway-us-east-2','apigateway-us-west-2','appstream-us-east-1','appstream2-us-east-1',
          'appstream2-us-west-2','athena-us-east-1','athena-us-east-2','athena-us-west-2','chime','clouddirectory-us-east-1','clouddirectory-us-east-2',
          'clouddirectory-us-west-2','cloudfront','cloudsearch-us-west-1','cloudsearch-us-east-1','cloudsearch-us-west-2','cloudwatch-ca-central-1',
          'cloudwatch-us-west-1','cloudwatch-us-east-1','cloudwatch-us-east-2','cloudwatch-us-west-2','cognito-us-east-1','cognito-us-east-2',
          'cognito-us-west-2','connect-us-east-1','dynamodb-ca-central-1','dynamodb-us-west-1','dynamodb-us-east-1','dynamodb-us-east-2',
          'dynamodb-us-west-2','dynamodb-dax-us-west-1','dynamodb-dax-us-east-1','dynamodb-dax-us-west-2','ecr-ca-central-1','ecr-us-west-1',
          'ecr-us-east-1','ecr-us-east-2','ecr-us-west-2','ecs-ca-central-1','ecs-us-west-1','ecs-us-east-1','ecs-us-east-2','ecs-us-west-2',
          'ec2systemsmanager-ca-central-1','ec2systemsmanager-us-west-1','ec2systemsmanager-us-east-1','ec2systemsmanager-us-east-2',
          'ec2systemsmanager-us-west-2','ec2-ca-central-1','ec2-us-west-1','ec2-us-east-1','ec2-us-east-2','ec2-us-west-2','elasticfilesystem-us-east-1',
          'elasticfilesystem-us-east-2','elasticfilesystem-us-west-2','elb-ca-central-1','elb-us-west-1','elb-us-east-1','elb-us-east-2','elb-us-west-2',
          'emr-ca-central-1','emr-us-west-1','emr-us-east-1','emr-us-east-2','emr-us-west-2','elastictranscoder-us-west-1','elastictranscoder-us-east-1',
          'elastictranscoder-us-west-2','elasticache-ca-central-1','elasticache-us-west-1','elasticache-us-east-1','elasticache-us-east-2',
          'elasticache-us-west-2','elasticsearch-ca-central-1','elasticsearch-us-west-1','elasticsearch-us-east-1','elasticsearch-us-east-2',
          'elasticsearch-us-west-2','gamelift-us-east-1','gamelift-us-west-2','glacier-ca-central-1','glacier-us-west-1',
          'glacier-us-east-1','glacier-us-east-2','glacier-us-west-2','inspector-us-west-1','inspector-us-east-1','inspector-us-west-2',
          'kinesis-ca-central-1','kinesis-us-west-1','kinesis-us-east-1','kinesis-us-east-2','kinesis-us-west-2','kinesisanalytics-us-east-1',
          'kinesisanalytics-us-west-2','firehose-us-east-1','firehose-us-west-2','lex-us-east-1','lightsail-us-east-1','lightsail-us-east-2',
          'lightsail-us-west-2','aml-us-east-1','analytics-us-east-1','pinpoint-us-east-1','polly-us-east-1','polly-us-east-2','polly-us-west-2',
          'redshift-ca-central-1','redshift-us-west-1','redshift-us-east-1','redshift-us-east-2','redshift-us-west-2','rekognition-us-east-1',
          'rekognition-us-west-2','rds-ca-central-1','rds-us-west-1','rds-us-east-1','rds-us-east-2','rds-us-west-2','route53',
          'route53domainregistration','route53-ca-central-1','route53-us-west-1','route53-us-east-1','route53-us-east-2',
          'route53-us-west-2','ses-us-east-1','ses-us-west-2','sns-ca-central-1','sns-us-west-1','sns-us-east-1','sns-us-east-2',
          'sns-us-west-2','sqs-ca-central-1','sqs-us-west-1','sqs-us-east-1','sqs-us-east-2','sqs-us-west-2','s3-ca-central-1',
          's3-us-west-1','s3-us-standard','s3-us-east-2','s3-us-west-2','swf-ca-central-1','swf-us-west-1','swf-us-east-1','swf-us-east-2','swf-us-west-2',
          'simpledb-us-west-1','simpledb-us-east-1','simpledb-us-west-2','vpc-ca-central-1','vpc-us-west-1','vpc-us-east-1','vpc-us-east-2',
          'vpc-us-west-2','workdocs-us-east-1','workdocs-us-west-2','workmail-us-east-1','workmail-us-west-2','workspaces-us-east-1',
          'workspaces-us-west-2','autoscaling-ca-central-1','autoscaling-us-west-1','autoscaling-us-east-1','autoscaling-us-east-2',
          'autoscaling-us-west-2','batch-us-east-1','batch-us-west-2','billingconsole-us-east-1','certificatemanager-ca-central-1',
          'certificatemanager-us-west-1','certificatemanager-us-east-1','certificatemanager-us-east-2','certificatemanager-us-west-2',
          'cloudformation-ca-central-1','cloudformation-us-west-1','cloudformation-us-east-1','cloudformation-us-east-2',
          'cloudformation-us-west-2','cloudhsm-ca-central-1','cloudhsm-us-west-1','cloudhsm-us-east-1','cloudhsm-us-east-2','cloudhsm-us-west-2',
          'cloudtrail-ca-central-1','cloudtrail-us-west-1','cloudtrail-us-east-1','cloudtrail-us-east-2','cloudtrail-us-west-2','codebuild-us-east-1',
          'codebuild-us-east-2','codebuild-us-west-2','codecommit-us-west-1','codecommit-us-east-1','codecommit-us-east-2',
          'codecommit-us-west-2','codedeploy-ca-central-1','codedeploy-us-west-1','codedeploy-us-east-1','codedeploy-us-east-2',
          'codedeploy-us-west-2','codepipeline-us-east-1','codepipeline-us-east-2','codepipeline-us-west-2','codestar-us-east-1','codestar-us-east-2',
          'codestar-us-west-2','config-ca-central-1','config-us-west-1','config-us-east-1','config-us-east-2','config-us-west-2','datapipeline-us-east-1',
          'datapipeline-us-west-2','dms-ca-central-1','dms-us-west-1','dms-us-east-1','dms-us-east-2','dms-us-west-2','devicefarm-us-west-2',
          'directconnect-ca-central-1','directconnect-us-west-1','directconnect-us-east-1','directconnect-us-east-2','directconnect-us-west-2',
          'directoryservice-ca-central-1','directoryservice-us-east-1','directoryservice-us-east-2','directoryservice-us-west-2',
          'elasticbeanstalk-ca-central-1','elasticbeanstalk-us-west-1','elasticbeanstalk-us-east-1','elasticbeanstalk-us-east-2',
          'elasticbeanstalk-us-west-2','awsgreengrass-us-east-1','awsgreengrass-us-west-2','iam-ca-central-1','iam-us-west-1','iam-us-east-1',
          'iam-us-east-2','iam-us-west-2','import-export','internetconnectivity-ca-central-1','internetconnectivity-us-west-1',
          'internetconnectivity-us-east-1','internetconnectivity-us-east-2','internetconnectivity-us-west-2','awsiot-us-east-1','awsiot-us-east-2',
          'awsiot-us-west-2','kms-ca-central-1','kms-us-west-1','kms-us-east-1','kms-us-east-2','kms-us-west-2','lambda-ca-central-1',
          'lambda-us-west-1','lambda-us-east-1','lambda-us-east-2','lambda-us-west-2','management-console','marketplace','mobilehub-us-east-1',
          'mobilehub-us-east-2','opsworkschef-us-east-1','opsworkschef-us-west-2','opsworks-us-west-1','opsworks-us-east-1','opsworks-us-east-2',
          'opsworks-us-west-2','organizations','quicksight-us-east-1','quicksight-us-east-2','quicksight-us-west-2',
          'resourcegroupstaggingapi-ca-central-1','resourcegroupstaggingapi-us-west-1','resourcegroupstaggingapi-us-east-1',
          'resourcegroupstaggingapi-us-east-2','resourcegroupstaggingapi-us-west-2','servicecatalog-ca-central-1','servicecatalog-us-east-1',
          'servicecatalog-us-east-2','servicecatalog-us-west-2','state-us-east-1','state-us-east-2','state-us-west-2','storagegateway-ca-central-1',
          'storagegateway-us-west-1','storagegateway-us-east-1','storagegateway-us-east-2','storagegateway-us-west-2','awswaf','xray-ca-central-1',
          'xray-us-west-1','xray-us-east-1','xray-us-east-2','xray-us-west-2'
        ]






#Divide east services / servers
services_us_east = []
easttz = pytz.timezone("US/Eastern")
for doc in services:
    if doc.endswith(('us-east-1','us-east-2')):
        services_us_east.append(doc)

#Divide west services / servers
services_us_west = []
westtz = pytz.timezone("US/Pacific")
for docw in services:
    if docw.endswith(('us-west-1','us-west-2')):
        services_us_west.append(docw)

#Connect/Create DB US EAST
client = MongoClient()
db = client.aws_us_east
posts = db.posts


def canIadd(newID):
    c = posts.find({'_id': newID}).count()
    if c == 0:
        return True
    else:
        return False

urls = []

for serv in services_us_east:
    #print "Populating and Updating database - " + serv
    urls.append( 'http://status.aws.amazon.com/rss/%s.rss' % (serv))


feed = feedparser.parse(urls)
#feed1 = feedparser.parse('http://status.aws.amazon.com/rss/state-us-east-1.rss')

for entry in feed.entries:
    print entry.id



#Get feed from corresponding api
#for serv in services_us_east:
#    print "Populating and Updating database - " + serv
#    feed = feedparser.parse('http://status.aws.amazon.com/rss/%s.rss' % (serv))
    #Organize data
#    for entry in feed.entries:
#        if canIadd(entry.id) == True:
#            s1 = entry.published[:-3].strip()
#            s2 = easttz.localize(datetime.strptime(s1, '%a, %d %b %Y %H:%M:%S'))
#            data = {
#            '_id' : entry.id,
#            'published' : s2,
#            'title' : entry.title,
#            'summary': entry.summary
#            }
            #Fill data if new
#            post_id = posts.insert_one(data).inserted_id
#            print("A new post has been added")

#for serv in services_us_west:
#    print "Populating and Updating database - " + serv
#    feed = feedparser.parse('http://status.aws.amazon.com/rss/%s.rss' % (serv))
    #Organize data
#    for entry in feed.entries:
#        if canIadd(entry.id):
#            print("A new post has been added")
#            s1 = entry.published[:-3].strip()
#            s2 = westtz.localize(datetime.strptime(s1, '%a, %d %b %Y %H:%M:%S'))
#            data = {
#            '_id' : entry.id,
#            'published' : s2,
#            'title' : entry.title,
#            'summary': entry.summary
#            }
            #Fill data if new
#            post_id = posts.insert_one(data).inserted_id


#curs = posts.find()
#for dat in curs:
#    print dat

end = time.time()
print "Updating time for NA region: " + str(end - start)
