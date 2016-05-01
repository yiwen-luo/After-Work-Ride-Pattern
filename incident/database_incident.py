from __future__ import print_function  # Python 2/3 compatibility
import boto3
import json
import decimal
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('../config.cfg')

dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")

def delete_database(table):
    try:
        table.delete()
    except Exception, e:
        raise e


def create_database(tablename):
    table = dynamodb.create_table(
        TableName=tablename,
        KeySchema=[
            {
                'AttributeName': 'time',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'order',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'time',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'order',
                'AttributeType': 'N'
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


def get_table(tablename):
    return dynamodb.Table(tablename)


def insert(table, item):
    response = table.put_item(
        Item={
            'incident': item["incident"],
            'time': item["time"],
            'order': item["order"],
            'longtitude':item["longtitude"],
            'latitude':item['latitude'],
            'company':item['company']
        }
    )
