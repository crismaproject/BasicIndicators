#!/usr/bin/env python

""" 
 receive events from orion Pub/Sup (XML POST requests)
 Calculate indicator values:
  lifeIndicator
 Send PubSub event about new data
"""

"""
    Copyright (C) 2014  AIT / Austrian Institute of Technology
    http://www.ait.ac.at
 
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 2 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
 
    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see http://www.gnu.org/licenses/gpl-2.0.html
"""

import os, sys
import json
import io
import requests
import string
import time

# list of indicators to calculate for each new worldstate
indicators = [
    'lifeIndicator', 
    'deathsIndicator',
    'seriouslyDeterioratedIndicator',
    'improvedIndicator'
    ]

# WPS service
wps = "http://crisma.ait.ac.at/indicators/pywps.cgi?service=WPS&request=Execute&version=1.0.0&identifier={}&datainputs=ICMMworldstateURL={}"

# The PubSub service-endpoint
orion="http://crisma.ait.ac.at/orion"

# The listener (this script!) endpoint
listener="http://crisma.ait.ac.at/indicators/OrionListener.py"

# the last registration id
subscriptionIdFile = "/home/crisma/public_html/indicators/subscription.json"

# if invoked as command: register as PubSub listener
if ((len (sys.argv) > 1) and ((sys.argv[1] == "--unsubscribe") or (sys.argv[1] == "--subscribe"))):
    # is there a subscription id from the last subscription stored? If so unsubscribe!
    if (os.path.exists (subscriptionIdFile)):
        # unsubscribe
        with io.open(subscriptionIdFile) as f:
            subscription = json.load(f)
            print "unsubscribe: "
            if ('subscribeResponse' in subscription):
                data = {
                    'subscriptionId' : subscription['subscribeResponse']['subscriptionId']
                    }
                params = {}
                headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
                response = requests.post("{}/NGSI10/unsubscribeContext".format (orion), data=json.dumps (data), params=params, headers=headers) 
                # unsubscription = response.json() if callable (response.json) else response.json
                print response.text
        os.remove (subscriptionIdFile)
    if (sys.argv[1] == "--subscribe"):
        print "subscribe: "
        # condValues was ["time"], but that is not ceccassary.
        data = {
            "entities": [
                {
                    "type": "CRISMA.worldstates",
                    "isPattern": "true",
                    "id": ".*"
                    }
                ],
            "reference": listener,
            "duration": "PT5M",
            "notifyConditions": [
                {
                    "type": "ONCHANGE",
                    "condValues": [
                        "dataslot_OOI-worldstate-ref"
                        ]
                    }
                ]
            }
        params = {}
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        response = requests.post("{}/NGSI10/subscribeContext".format (orion), data=json.dumps (data), params=params, headers=headers) 
        # subscription = response.json() if callable (response.json) else response.json
        with io.open (subscriptionIdFile, "w") as f:
            f.write (response.text)
        print response.text
    exit (0)


# code to be executed if invoced as CGI script

print "Content-Type: text/plain"    # HTML is following
print                               # blank line, end of headers
print "<!-- The OrionBroker Listener says: Thanks for your message -->"


# os.getenv("QUERY_STRING")

data = sys.stdin.read()

print >>sys.stderr, "\n\n"
print >>sys.stderr, data 
print >>sys.stderr, "\n\n"


# since subscription was done using json the notification is also formatted as json

notification = json.loads (data)

elems = notification["contextResponses"]

for elem in elems:
    for attr in elem["contextElement"]["attributes"]:
        if attr["name"].startswith ("worldstate"):
            wsURL = attr["value"]["URI"]
            for indicator in indicators:
                print >>stderr, "Start indicator {} for {}".format (indicator, wsURL)
                response = requests.get(wps.format (indicator, wsURL))
                print >>stderr, response.text
            

exit (0)


exampleNotification = {
   "subscriptionId" : "5357b2b3000000dea5adf59d",
   "originator" : "localhost",
   "contextResponses" : [
     {
       "contextElement" : {
         "type" : "CRISMA.worldstates",
         "isPattern" : "false",
         "id" : "1_2",
         "attributes" : [
           {
             "name" : "time",
             "type" : "",
             "value" : "1398256494"
           },
           {
             "name" : "worldstate_Baseline",
             "type" : "Test baseline",
             "value" : "{\\"operation\\":\\"updated\\",\\"time\\":1398256494,\\"URI\\":\\"http://crisma.cismet.de/pilotC/icmm_api/CRISMA.worldstates/2\\"}"
           },
           {
             "name" : "dataslot_OOI-worldstate-ref",
             "type" : "Test baseline",
             "value" : "{\\"operation\\":\\"created\\",\\"time\\":1398256492,\\"URI\\":\\"http://crisma.cismet.de/pilotC/icmm_api/CRISMA.dataitems/3\\"}"
           }
         ]
       },
       "statusCode" : {
         "code" : "200",
         "reasonPhrase" : "OK"
       }
     }
   ]
 }

