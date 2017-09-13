from pymongo import MongoClient
import datetime


client = MongoClient()
db = client.aws_us_east
posts = db.posts

#Find by region
#f = posts.find({"_id":{'$regex' : ".*-us-east"}})
#for post in f:
#    print post


#Find by timeframe
#start = datetime.datetime(2016, 9, 14, 1, 31, 0, 0)
#end = datetime.datetime(2016, 9, 14, 1, 32, 0, 0)

start = 'Thu,  9 Feb 2017 19:29:00 PST'
#'Thu,  9 Feb 2017 19:29:00 PST'

d = posts.find({"published": start})
for doc in d:
    print doc
