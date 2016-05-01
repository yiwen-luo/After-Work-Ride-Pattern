# -*- coding: utf-8 -*-
from __future__ import print_function # Python 2/3 compatibility
import requests
import json
import time
import boto3
import database
import ConfigParser
import decimal
import urllib2, urllib


# load config file
config = ConfigParser.RawConfigParser()
config.read('../config.cfg')

#with open('location.json') as data_file:    
#   data = json.load(data_file)
#company = data["places"][0] # for test 


# read table name
tablename = "uber_weather"

# create database if not exist
#dynamodb_table = database.create_database(tablename)

dynamodb_table = database.get_table(tablename)
order = 0
while True:
    order = order + 1
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select item.condition from weather.forecast where woeid = 12761478"
    yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
    result = urllib2.urlopen(yql_url).read()
    preprocess_data = json.loads(result)
    try:
    	weather = preprocess_data['query']['results']['channel']['item']['condition']['text'].encode('utf-8')
    except:
	continue
	
    Time = preprocess_data['query']['results']['channel']['item']['condition']['date'].encode('utf-8')
    
    # insert into dynamodb 
    item = {"weather":weather,"time":Time,"order":order}
    print(item)
    database.insert(dynamodb_table, item)            

    time.sleep(600)
