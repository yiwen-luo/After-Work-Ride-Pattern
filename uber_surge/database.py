from __future__ import print_function  # Python 2/3 compatibility
import boto3
import json
import decimal
import ConfigParser

# access config information
config = ConfigParser.RawConfigParser()
config.read('../config.cfg')

# get access to dynomodb
dynamodb = boto3.resource('dynamodb', region_name=config.get('dynamo', 'region_name'), endpoint_url=config.get('dynamo', 'endpoint_url'))

# for the use to delete the database
def delete_database(table):
    try:
        table.delete()
    except Exception, e:
        raise e

# create a dynamodb table
def create_database(tablename):
    table = dynamodb.create_table(
        TableName=tablename,
        KeySchema=[
            {
                'AttributeName': 'name',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'time',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'time',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    print("Table %s is creating" % tablename)
    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName=tablename)

    print("Table status: %s" % table.table_status)
    return table


# access the database table
def get_table(tablename):
    return dynamodb.Table(tablename)


# wrapper function to insert item into table, data format specified
def insert(table, item):
    response = table.put_item(
        Item={
            'name': item["name"],
            'time': item["time"],
            'surge_multiplier': item["surge_multiplier"],
            'lat': item["lat"],
            'lon': item["lon"]
        }
    )