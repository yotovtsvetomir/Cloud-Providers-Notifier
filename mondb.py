from pymongo import MongoClient
import datetime
import pprint
import feedparser


client = MongoClient()
db = client.aws_us_east
posts = db.posts

neww = "http://status.aws.amazon.com/#apigateway-us-east-1_1498205520"


def canIadd(newID):
    c = posts.find({'_id': newID}).count()
    if c == 0:
        return True
    else:
        return False


for dd in posts.find():
    if canIadd(neww):
        print "I will add this"
