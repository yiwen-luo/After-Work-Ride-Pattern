from __future__ import print_function # Python 2/3 compatibility
import requests
import json
import time
import boto3
import database
import ConfigParser


# load config file
config = ConfigParser.RawConfigParser()
config.read('../config.cfg')

# get favored locations' information
with open('location.json') as data_file:    
    location = json.load(data_file)

# uber surge data get
server_token = config.get('dynamo', 'server_token')
uber_url = config.get('uber_api', 'uber_url')

# read table name
tablename = "storytelling"

# create database if not exist
# dynamodb_table = database.create_database(tablename)

dynamodb_table = database.get_table(tablename)

while True:
    # infinite loop 
    for company in location["places"]:
        # set api parameters
        start_latitude = end_latitude = company["lat"]
        start_longitude = end_longitude = company["lon"]
        parameters = {
            'server_token': server_token,
            'start_latitude': start_latitude,
            'end_latitude': end_latitude,
            'start_longitude': start_longitude,
            'end_longitude': end_longitude
        }
        response = requests.get(uber_url, params=parameters)
        data = response.json()
        # retrieve data
        for price in data["prices"]:
            if price["display_name"] == "uberX":
                # create item and insert into dynamodb 
                item = json.loads('{"name":"%s","time":"%s","surge_multiplier":"%s","lat":"%s","lon":"%s"}' % (company["name"], time.time(), price["surge_multiplier"], start_latitude, start_longitude), )
                print(item)
                database.insert(dynamodb_table, item)            
        time.sleep(5)

