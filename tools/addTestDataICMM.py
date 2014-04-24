#!/usr/bin/env python
#
# Start from parent directory with:
# PYTHONPATH="wps/processes" tools/addTestDataICMM.py



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

import ICMMtools as ICMM



def upload (ICMMworldstateURL, data):
     ICMMworldstate = ICMM.ICMMAccess (ICMMworldstateURL)
     ICMMindicatorValueURL = ICMM.addIndicatorValToICMM (ICMMworldstate.id, data['id'], data['description'], data, ICMMworldstate.endpoint)
     return ICMMindicatorValueURL


####################

print upload ("http://crisma.cismet.de/pilotC/icmm_api/CRISMA.worldstates/2", indicator81A)
print upload ("http://crisma.cismet.de/pilotC/icmm_api/CRISMA.worldstates/2", indicator81B)
print upload ("http://crisma.cismet.de/pilotC/icmm_api/CRISMA.worldstates/3", indicator82A)
print upload ("http://crisma.cismet.de/pilotC/icmm_api/CRISMA.worldstates/3", indicator82B)

