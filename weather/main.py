# -*- coding: utf-8 -*-
from __future__ import print_function # Python 2/3 compatibility
import requests
import json
import time
import boto3
import database
import ConfigParser
import decimal
import urllib2, urllib   #import kinds of libraries




# read table name
tablename = "uber_weather"

# create database if not exist
# dynamodb_table = database.create_database(tablename)

dynamodb_table = database.get_table(tablename)  # first, get the table
order = 0  # initialize order to 0
# start the loop

while True:
    order = order + 1  # update order 
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select item.condition from weather.forecast where woeid = 12761478"   # use yahoo query sentence to get manhattan weather
    yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"   # constitute the url to request
    result = urllib2.urlopen(yql_url).read()  # get the result returned by yahoo_weather api
    preprocess_data = json.loads(result)   # transform result from json format to python dictionary format
    try:
    	weather = preprocess_data['query']['results']['channel']['item']['condition']['text'].encode('utf-8')  # try to get weather result
    except:
	    continue
	
    Time = preprocess_data['query']['results']['channel']['item']['condition']['date'].encode('utf-8')   # extract time information
    
    # insert into dynamodb 
    item = {"weather":weather,"time":Time,"order":order}   # create new item 
    print(item)  
    database.insert(dynamodb_table, item) # insert new item into our dynamodb--uber_weather            

    time.sleep(600) # wait 10 minutes and fetch and insert item again because weather data is normally updated one hour
