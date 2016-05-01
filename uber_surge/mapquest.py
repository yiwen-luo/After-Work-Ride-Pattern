import requests
import ConfigParser


def getBoundingBox(latitude, longitude, milesFromCenter):  
    # format parameter string for the access of bouding box
    # given lat, lon and radius in miles, return the bounding box of square size
    approxLatDegreeMiles = 69
    approxLonDegreeMiles = 53
  
    #calculate upper left
    ulLat = latitude + float(milesFromCenter) / float(approxLatDegreeMiles)
    ulLon = longitude + float(milesFromCenter) / float(approxLonDegreeMiles)

    #calculate lower right
    lrLat = latitude - float(milesFromCenter) / float(approxLatDegreeMiles)
    lrLon = longitude - float(milesFromCenter) / float(approxLonDegreeMiles)

    box = str(ulLat) + "," + str(ulLon) + "," + str(lrLat) + "," + str(lrLon)

    return box

# load config file
config = ConfigParser.RawConfigParser()
config.read('../config.cfg')

key = config.get('mapquest_api', 'key')

# test for Goldman Sachs' building 
# get construction and incident data 
response = requests.get(url = "http://www.mapquestapi.com/traffic/v2/incidents?key=" + key + "&boundingBox=" + getBoundingBox(40.715082, -74.014390, 1.5) + "&filters=construction,incidents&inFormat=kvp&outFormat=json")
data = response.json()

print data["incidents"][0]

