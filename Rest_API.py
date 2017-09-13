#!flask/bin/python
import feedparser
import json
from pymongo import MongoClient
import pytz
from dateutil.tz import tzutc, tzlocal
from datetime import datetime
import time
import shte
from flask import Flask, jsonify
from flask import render_template
from flask import request

app = Flask(__name__)

client = MongoClient()
aws = client.aws
gcloud = client.gcloud
azure = client.azure


@app.route('/v1/', methods=['GET'])
@app.route('/', methods=['GET'])
def get_index():
    name = None
    return render_template('index.html', name=name)

@app.route('/v1/aws', methods=['GET'])
def get_aws():
        output = shte.getAwsAll()
        return jsonify({'Results sorted by region' : output})

@app.route('/v1/gcloud', methods=['GET'])
def get_gcloud():
    output = []
    gc = gcloud.posts.find().sort('published', -1)
    for c in gc:
        output.append(c)
    return jsonify({'Results sorted by date' : output})

@app.route('/v1/azure', methods=['GET'])
def get_azure():
    output = []
    az = azure.posts.find().sort('published', -1)
    for a in az:
        output.append(a)
    return jsonify({'Results sorted by date' : output})

@app.route('/v1/aws/<region>/',methods=['GET'])
def get_region(region):
    output = []
    if region == "na":
        tr = aws.naposts.find().sort('published', -1)
        for s in tr:
            output.append(s)
    elif region == "sa":
        tr = aws.saposts.find().sort('published', -1)
        for s in tr:
            output.append(s)
    elif region == "asia":
        tr = aws.asiaposts.find().sort('published', -1)
        for s in tr:
            output.append(s)
    elif region == "eu":
        tr = aws.euposts.find().sort('published', -1)
        for s in tr:
            output.append(s)

    return jsonify({'Results sorted by date and region' : output})


@app.route('/v1/aws/<region>/<service>',methods=['GET'])
def getbyRandG(region,service):
    output = shte.getByRegionAndService(region,service)
    return jsonify({'Results sorted by date, region: ' + region + ', serivce: ' + service  : output})

#@app.route('/v1/aws/<region>/<service>/',methods=['GET'])
#def getbyPeriod():


if __name__ == '__main__':
     app.run(debug=True, port = 7777)
