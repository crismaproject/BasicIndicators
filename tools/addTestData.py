#!/usr/bin/env python

indicator81A = {
    "id":"timeIntervalsTest",
    "name":"Just some test data",
    "description":"List of time intervals",
    "worldstates":[81],
    "type":"timeintervals",
    "data": {
        "intervals": [
            {
                "startTime": "2012-01-01T12:19:00.000",
                "endTime": "2012-01-01T12:24:00.000",
                },
            {
                "startTime": "2012-01-01T12:41:00.000",
                "endTime": "2012-01-01T12:42:00.000",
                }
            ],
        "color": "#00cc00",
        "linewidth": 2
        }
    }

indicator82A = {
    "id":"timeIntervalsTest",
    "name":"Just some test data",
    "description":"List of time intervals",
    "worldstates":[82],
    "type":"timeintervals",
    "data": {
        "intervals": [
            {
                "startTime": "2012-01-01T12:19:00.000",
                "endTime": "2012-01-01T12:24:00.000",
                },
            {
                "startTime": "2012-01-01T12:41:00.000",
                "endTime": "2012-01-01T12:45:00.000",
                }
            ],
        "color": "#00cc00",
        "linewidth": 2
        }
    }

indicator81B = {
    "id":"timeIntervalsTest2",
    "name":"Just some other test data",
    "description":"List of time intervals",
    "worldstates":[82],
    "type":"timeintervals",
    "data": {
        "intervals": [
            {
                "startTime": "2012-01-01T12:10:00.000",
                "endTime": "2012-01-01T12:12:00.000",
                }
            ],
        "color": "#0000cc",
        "linewidth": 2
        }
    }

indicator82B = {
    "id":"timeIntervalsTest2",
    "name":"Just some other test data",
    "description":"List of time intervals",
    "worldstates":[82],
    "type":"timeintervals",
    "data": {
        "intervals": [
            {
                "startTime": "2012-01-01T12:10:00.000",
                "endTime": "2012-01-01T12:19:00.000",
                }
            ],
        "color": "#0000cc",
        "linewidth": 2
        }
    }


#########################################3

from sys import stderr
import json
import requests

indicatorEntityId = 101
baseUrl = 'http://crisma-ooi.ait.ac.at/api/EntityProperty'



def upload (worldStateId, indicatorPropertyId, data):
     indicatorValue = json.dumps (data)
     indicatorProperty = {
         "entityId" : indicatorEntityId,
         "entityTypePropertyId": indicatorPropertyId,
         "entityPropertyValue": indicatorValue,
         "worldStateId": worldStateId,
         }
     # check if there is already an entry
     params = {
         'wsid' :  worldStateId, 
         'etpid' : indicatorPropertyId
         }
     indicatorProperties = requests.get(baseUrl, params=params) 
        
     if indicatorProperties.status_code != 200:
         return "Error accessing WorldState with id {}: {}".format (worldStateId, indicatorProperties.raise_for_status())
     
     # count already existing results
     existingResults = 0;
     existingResult = None
     for ep in indicatorProperties.json:
         # print "{}: {}".format (indicatorProperties, ep)
         existingResults +=1
         if existingResults > 1:
             return "There are already {} results! This should not be the case!".format (existingResults)
         if existingResults == 1:
             existingResult = indicatorProperties.json[0]['entityPropertyId']
             # Select what you want:
             # ## option 1: This is an error
             #return "There is already a result!"
             # ## option 2: not an error, just use existing result
             #resultUrl = "{}/{}".format (baseUrl, existingResult)
             #self.Answer.setValue(escape (resultUrl))
             #return
             # ## option 3: not an error, recalculate and replace
             pass

     if existingResults == 1:
         indicatorProperty["entityPropertyId"] = existingResult
         print >> stderr, "put to {}/{}".format (baseUrl, existingResult)
         result = requests.put ("{}/{}".format (baseUrl, existingResult), data=json.dumps (indicatorProperty), headers={'content-type': 'application/json'})
         if result.status_code != 200:
             return "Unable to PUT result at {}/{}: {}".format (baseUrl, existingResult, result.status_code)
         resultUrl = "{}/{}".format (baseUrl, existingResult)
     else:
         print >> stderr, "post to{}".format (baseUrl)
         result = requests.post (baseUrl, data=json.dumps (indicatorProperty), headers={'content-type': 'application/json'})
         if result.status_code != 201:
             return "Unable to POST result at {}: {}".format (baseUrl, result.status_code)
         newResult = result.json[u'entityPropertyId']
         resultUrl = "{}/{}".format (baseUrl, newResult)
     return resultUrl

####################

print upload (81, 64, indicator81A)
print upload (81, 65, indicator81B)
print upload (82, 64, indicator82A)
print upload (82, 65, indicator82B)

