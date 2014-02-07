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
from lxml import etree
import requests
import string
import time
from sys import stderr

print "Content-Type: text/plain"    # HTML is following
print                               # blank line, end of headers
print "<!-- The OrionBroker Listener says: Thanks for your message -->"

# os.getenv("QUERY_STRING")

data = sys.stdin.read()

#print >>stderr, "\n\n"
#print >>stderr, data 
#print >>stderr, "\n\n"


root = etree.fromstring (data)

# root.tag might be:
# <notifyContextAvailabilityRequest> : New WorldState
# <notifyContextRequest>: OOI changed
print >>stderr, "OrionListener got a {}".format (root.tag)

# Example:
#
# <notifyContextRequest>
#   <subscriptionId>52efb40c0000000cf18e0248</subscriptionId>
#   <originator>localhost</originator>
#   <contextResponseList>
#     <contextElementResponse>
#       <contextElement>
#         <entityId type="WorldState" isPattern="false">
#           <id>75</id>
#         </entityId>
#         <contextAttributeList>
#           <contextAttribute>
#             <name>creation</name>
#             <type>creation</type>
#             <contextValue>1391441007</contextValue>
#           </contextAttribute>
#         </contextAttributeList>
#       </contextElement>
#       <statusCode>
#         <code>200</code>
#         <reasonPhrase>OK</reasonPhrase>
#       </statusCode>
#     </contextElementResponse>
#   </contextResponseList>
# </notifyContextRequest>



wps = "http://crisma.ait.ac.at/indicators/pywps.cgi?service=WPS&request=Execute&version=1.0.0&identifier=lifeIndicator&datainputs=WorldStateId={}"
orion = "http://crisma.ait.ac.at/orion/NGSI10/updateContext"

if "notifyContextRequest" == root.tag:
    # We are only registered for "creation" updates, so no need to check for this
    # new WorldState
    # trigger indicator calculation
    idElem = root.find ("./contextResponseList/contextElementResponse/contextElement/entityId/id")
    wsid = idElem.text
    response = requests.get(wps.format (wsid))
    print >>stderr, response.text
    xmlheaderlen = len ('<?xml version="1.0" encoding="utf-8"?>')
    result = etree.fromstring (response.text[xmlheaderlen:])
    # successElem = result.find ("{http://www.opengis.net/wps/1.0.0}ExecuteResponse/{http://www.opengis.net/wps/1.0.0}Status/{http://www.opengis.net/wps/1.0.0}ProcessSucceeded")
    successElem = result.find (".//{http://www.opengis.net/wps/1.0.0}ProcessSucceeded")
    if successElem is not None:
        # dataElem = result.find ("{http://www.opengis.net/wps/1.0.0}ExecuteResponse/{http://www.opengis.net/wps/1.0.0}ProcessOutputs/{http://www.opengis.net/wps/1.0.0}Output/{http://www.opengis.net/wps/1.0.0}Data/{http://www.opengis.net/wps/1.0.0}LiteralData")
        dataElem = result.find (".//{http://www.opengis.net/wps/1.0.0}LiteralData")
        uri = dataElem.text
        # print >>stderr, uri
        
        # ooiid = uri[string.rfind (uri, '/')+1:]

        # print >>stderr, ooiid

        psRequest = """<?xml version="1.0" encoding="UTF-8"?>
<updateContextRequest>
  <contextElementList>
    <contextElement>
      <entityId type="WorldState" isPattern="false">
        <id>{}</id>
      </entityId>
      <contextAttributeList>
        <contextAttribute>
          <name>lifeIndicator</name>
          <type>indicator</type>
          <contextValue>{} {}</contextValue>
        </contextAttribute>
      </contextAttributeList>
    </contextElement>
  </contextElementList>
  <updateAction>APPEND</updateAction>
</updateContextRequest>""".format (wsid, time.time(), uri)

        #print >>stderr, psRequest
        
        # (curl $endpoint/NGSI10/updateContext -s -S --header 'Content-Type: application/xml' -d @- | xmllint --format - ) <<EOF

        answer = requests.post (orion, data=psRequest, headers={'Content-Type' : 'application/xml'})

        #print >>stderr, answer.text


