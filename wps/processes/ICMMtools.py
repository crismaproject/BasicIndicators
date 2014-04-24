#!/usr/bin/env python
#
# Peter.Kutschera@ait.ac.at, 2014-03-13
# Time-stamp: "2014-04-24 15:01:02 peter"
#
# Tools to access ICMM

######################
#  Configuration
defaultBaseUrl = 'http://crisma.cismet.de/pilotC/icmm_api'
defaultDomain = 'CRISMA'
#####################

import json
import requests
import re
#import time
import datetime
import math
import logging

class ICMMAccess:
    def __init__ (self, url):
        """crunch ICMM URL into endpoint, domain, clazz, id

        url: 'http://crisma.cismet.de/pilotC/icmm_api/CRISMA.worldstates/1?ignored=parameters

        result:
         endpoint=https://crisma.cismet.de/pilotC/icmm_api, 
         domain=CRISMA, 
         clazz=worldstates, 
         id=1
        """
        self.url = url
        self.endpoint = None
        self.domain = None
        self.clazz = None
        self.id = None
        if (url is not None):
            match = re.search ("(https?://.*)/([^.]+)\.([^.]+)/([0-9]+)(\?.*)?$", url)
            if (match):
                self.endpoint = match.group(1)
                self.domain = match.group(2)
                self.clazz = match.group(3)
                self.id = int (match.group(4))

    def __repr__ (self):
        return "endpoint={}, domain={}, clazz={}, id={}".format (self.endpoint, self.domain, self.clazz, self.id)


def getId (clazz, baseUrl=defaultBaseUrl, domain=defaultDomain):
    """Get the next available id for the given class

    clazz: class name within ICMM
    """
    params = {
        'limit' :  999999999
        }
    headers = {'content-type': 'application/json'}
    response = requests.get("{}/{}.{}".format (baseUrl, domain, clazz), params=params, headers=headers) 
    # this was the request:
    # print response.url

    if response.status_code != 200:
        raise Exception ( "Error accessing ICMM at {}: {}".format (response.url, response.raise_for_status()))

    # Depending on the requests-version json might be an field instead of on method
    # print response.json()
    jsonData = response.json() if callable (response.json) else response.json

    maxid = 0;
    collection = jsonData['$collection']
    for r in collection:
        ref = r['$ref']
        match = re.search ("/([0-9]+)$", ref)
        if (match):
            id = int (match.group(1))
            if (id > maxid):
                maxid = id
    return maxid + 1


def getNameDescription (wsid, baseUrl=defaultBaseUrl, domain=defaultDomain):
    """Get name and description of worldstate id
    
    """
    # http://crisma.cismet.de/pilotC/icmm_api/CRISMA.worldstates/3?level=1&fields=name%2Cdescription&omitNullValues=true&deduplicate=true
    # get (grand*)parent worldstate list
    params = {
        'level' :  1,
        'fields' : "name,description",
        'omitNullValues' : 'true',
        'deduplicate' : 'true'
        }
    headers = {'content-type': 'application/json'}
    response = requests.get("{}/{}.{}/{}".format (baseUrl, domain, "worldstates", wsid), params=params, headers=headers) 

    if response.status_code != 200:
        raise Exception ("Error accessing ICMM at {}: {}".format (response.url, response.status_code))
    if response.text is None:
        raise Exception ("No such ICMM WorldState")
    if response.text == "":
        raise Exception ("No such ICMM WorldState")

    # Depending on the requests-version json might be an field instead of on method
    worldstate = response.json() if callable (response.json) else response.json
    return {
        'ICMMname' : worldstate["name"],
        'ICMMdescription' : worldstate["description"]
        }

def getBaseWorldstate (wsid, baseCategory="Baseline", baseUrl=defaultBaseUrl, domain=defaultDomain):
    """Get parent worldstate id with given category or None
    
    default baseCategory: "Baseline". Other posibilities: "Template"
    """
    # http://crisma.cismet.de/pilotC/icmm_api/CRISMA.worldstates/3?level=1000&fields=parentworldstate%2Ccategories&omitNullValues=true&deduplicate=true
    # get (grand*)parent worldstate list
    params = {
        'level' :  1000,
        'fields' : "parentworldstate,categories,key,id",
        'omitNullValues' : 'true',
        'deduplicate' : 'true'
        }
    headers = {'content-type': 'application/json'}
    response = requests.get("{}/{}.{}/{}".format (baseUrl, domain, "worldstates", wsid), params=params, headers=headers) 

    if response.status_code != 200:
        raise Exception ("Error accessing ICMM at {}: {}".format (response.url, response.status_code))
    if response.text is None:
        raise Exception ("No such ICMM WorldState")
    if response.text == "":
        raise Exception ("No such ICMM WorldState")

    # Depending on the requests-version json might be an field instead of on method
    worldstate = response.json() if callable (response.json) else response.json
    while (True):
        if ('categories' in worldstate):
            for c in worldstate['categories']:
                if c['key'] == baseCategory:                
                    return worldstate['id']
        if ('parentworldstate' not in worldstate):
            return None
        worldstate =  worldstate['parentworldstate']
    return None # never reach this, just to see the end of the function.

def getOOIRef (wsid, category, name=None, baseUrl=defaultBaseUrl, domain=defaultDomain):
    """Get the OOI reference within a dataitem contained in an ICMM worldstate

    wsid: ICMM worldstate id
    category: key of the category of the requested dataitem
    name: id of indicator (None if this does not matter)
    """
    # get WorldState
    params = {
        'level' :  3,
        'fields' : "worldstatedata,actualaccessinfo,key,categories,datadescriptor,defaultaccessinfo,name",
        'omitNullValues' : 'true',
        'deduplicate' : 'false'
        }
    headers = {'content-type': 'application/json'}
    response = requests.get("{}/{}.{}/{}".format (baseUrl, domain, "worldstates", wsid), params=params, headers=headers) 

    if response.status_code != 200:
        raise Exception ("Error accessing ICMM at {}: {}".format (response.url, response.status_code))
    if response.text is None:
        raise Exception ("No such ICMM WorldState")
    if response.text == "":
        raise Exception ("No such ICMM WorldState")

    # Depending on the requests-version json might be an field instead of on method
    worldstate = response.json() if callable(response.json) else response.json

    dataitems = worldstate['worldstatedata']
    for d in dataitems:
      if ((name is None) or (name == d['name'])):
        if ('categories' in d):
            for c in d['categories']:
                if c['key'] == category:
                    access = json.loads (d['actualaccessinfo'])
                    service = json.loads (d['datadescriptor']['defaultaccessinfo'])
                    return "{}/{}/{}".format(service['endpoint'], access['resource'], access['id'])
    return None

def addIndicatorRefToICMM (wsid, name, description, ooiref, baseUrl=defaultBaseUrl, domain=defaultDomain):
    """Add an reference to an indicator value stored in the OOS-WSR

    wsid: id within ICMM
    ooiref: URL into OOI-WSR

    returns: ICMM indicator URL (dataitem)
    """
    # Get worldstate 
    ICMMindicatorURL = None
    params = {
        'level' :  2,
        'fields' : "worldstatedata,name,categories",
        'omitNullValues' : 'true',
        'deduplicate' : 'true'
        }
    headers = {'content-type': 'application/json'}
    response = requests.get("{}/{}.{}/{}".format (baseUrl, domain, "worldstates", wsid), params=params, headers=headers) 

    if response.status_code != 200:
        raise Exception ("Error accessing ICMM at {}: {}".format (response.url, response.raise_for_status()))
    if response.text is None:
        raise Exception ("No such ICMM WorldState")
    if response.text == "":
        raise Exception ("No such ICMM WorldState")

    # Depending on the requests-version json might be an field instead of on method
    worldstate = response.json() if callable (response.json) else response.json

    # check if the indicator is already in the ICMM worldstate
    if (worldstate['worldstatedata'] is not None):
        for d in worldstate['worldstatedata']:
            if ('categories' in d):
                for c in d['categories']:
                    if ((c['$ref'] == "/{}.categories/3".format (domain)) and (d['name'] == name)):
                        ICMMindicatorURL = "{}{}".format (baseUrl, d['$self'])
                        return ICMMindicatorURL
                        
    # not found, do some work...

    # add dataitem to worldstate
    #   I need a new dataitems id
    dataitemsId = getId ("dataitems");
    # t = time.time() * 1000
    t = datetime.datetime.utcnow().isoformat()

    data = {
        "$self": "/{}.dataitems/{}".format (domain, dataitemsId),
        "id": dataitemsId,
        "name": name,
        "description": description,
        "categories": [
            {
                "$ref": "/{}.categories/3".format (domain)
            }
        ],
        "datadescriptor": {
            "$ref": "/{}.datadescriptors/1".format (domain)
            },
        "actualaccessinfocontenttype": "URL",
        "actualaccessinfo": ooiref,
        "lastmodified": t
        }

    if ('worldstatedata' in worldstate):
        worldstate['worldstatedata'].append (data)
    else:
        worldstate['worldstatedata'] = [ data ]

    # store worldstate back
    params = {
        'level' :  1,
        'fields' : "worldstatedata",
        'omitNullValues' : 'true',
        'deduplicate' : 'true'
        }
    response = requests.put("{}/{}.{}/{}".format (baseUrl, domain, "worldstates", wsid), params=params, headers=headers, data=json.dumps (worldstate)) 

    if response.status_code != 200:
        raise Exception ("Error writing worldstate to ICMM at {}: {}".format (response.url, response.raise_for_status()))
    
    # That is now stored in ICMM: response.json()

    ICMMindicatorURL = "{}/{}.dataitems/{}".format (baseUrl, domain, dataitemsId)
    return ICMMindicatorURL    



def addIndicatorValToICMM (wsid, name, description, value, baseUrl=defaultBaseUrl, domain=defaultDomain):
    """Add an indicator value 

    wsid: id within ICMM
    value: indicator-value as json structure

    returns: ICMM indicator URL (dataitem)
    """
    # Get worldstate 
    ICMMindicatorURL = None
    params = {
        'level' :  2,
        'fields' : "worldstatedata,name,categories",
        'omitNullValues' : 'true',
        'deduplicate' : 'true'
        }
    headers = {'content-type': 'application/json'}
    response = requests.get("{}/{}.{}/{}".format (baseUrl, domain, "worldstates", wsid), params=params, headers=headers) 

    if response.status_code != 200:
        raise Exception ("Error accessing ICMM at {}: {}".format (response.url, response.raise_for_status()))
    if response.text is None:
        raise Exception ("No such ICMM WorldState")
    if response.text == "":
        raise Exception ("No such ICMM WorldState")

    # Depending on the requests-version json might be an field instead of on method
    worldstate = response.json() if callable (response.json) else response.json

    # t = time.time() * 1000
    t = datetime.datetime.utcnow().isoformat()

    ICMMindicatorURL = None
    # check if the indicator is already in the ICMM worldstate
    if (worldstate['worldstatedata'] is not None):
        for d in worldstate['worldstatedata']:
            if ('categories' in d):
                for c in d['categories']:
                    if ((c['$ref'] == "/{}.categories/4".format (domain)) and (d['name'] == name)):
                        # An indicator value with the given name is already there - TODO: update value
                        d['actualaccessinfo'] = json.dumps (value)
                        d["lastmodified"] = t
                        ICMMindicatorURL = "{}{}".format (baseUrl, d['$self'])
    
    if (ICMMindicatorURL is None):
        # not found, do some work...

        # add dataitem to worldstate
        #   I need a new dataitems id
        dataitemsId = getId ("dataitems");
        
        data = {
            "$self": "/{}.dataitems/{}".format (domain, dataitemsId),
            "id": dataitemsId,
            "name": name,
            "description": description,
            "categories": [
                {
                    "$ref": "/{}.categories/4".format (domain)
                    }
                ],
            "datadescriptor": {
                "$ref": "/{}.datadescriptors/1".format (domain)
                },
            "actualaccessinfocontenttype": "application/json",
            "actualaccessinfo": json.dumps (value),
            "lastmodified": t
            }
        
        if ('worldstatedata' in worldstate):
            worldstate['worldstatedata'].append (data)
        else:
            worldstate['worldstatedata'] = [ data ]
        ICMMindicatorURL = "{}/{}.dataitems/{}".format (baseUrl, domain, dataitemsId)
    else:
        # worldstate['worldstatedata'] already updated up there: d['actualaccessinfo'] = json.dumps (value)
        pass


    # store worldstate back
    params = {
        'level' :  1,
        'fields' : "worldstatedata",
        'omitNullValues' : 'true',
        'deduplicate' : 'true'
        }
    response = requests.put("{}/{}.{}/{}".format (baseUrl, domain, "worldstates", wsid), params=params, headers=headers, data=json.dumps (worldstate)) 

    if response.status_code != 200:
        raise Exception ("Error writing worldstate to ICMM at {}: {}".format (response.url, response.raise_for_status()))
    # This is now stored in ICMM: response.json()

    return ICMMindicatorURL    





if __name__ == "__main__":
    for c in ["worldstates", "transitions", "dataitems"]:
        print "{}: {}".format (c, getId (c)) 
    # print addIndicatorRefToICMM (1, "testIndicator", "description of test indicator", {"id":193838, "resource":"EntityProperty"}) 
    # print getOOIRef (1, 'OOI-worldstate-ref')  # http://crisam-ooi.ait.ac.at/api/worldstate/335
    # print getOOIRef (2, 'OOI-worldstate-ref')  # Exception: No such ICMM WorldState
    # print getOOIRef (67, 'OOI-worldstate-ref') # None
    # print getOOIRef (1, 'OOI-indicator-ref', 'testIndicator') # http://crisam-ooi.ait.ac.at/api/EntityProperty/193838
    print addIndicatorValToICMM (2, "testIndicatorValue", "description of test indicator", 
                                 {"id": "testIndicatorValue",
                                  "name": "test value",
                                  "description": "Some Description",
                                  "worldstateDescription": {"ICMMworldstateURL": "http://crisma.cismet.de/pilotC/icmm_api/CRISMA.worldstates/2", "ICMMdescription": "This is a test baseline.", "ICMMname": "Test baseline"}, 
                                  "type": "number",
                                  "data": 50
                                  })

