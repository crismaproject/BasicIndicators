#!/bin/bash
#
# Peter Kutschera, Thu Feb  6 12:42:00 2014
# Time-stamp: "2014-02-07 08:15:00 peter"

#    Copyright (C) 2014  AIT / Austrian Institute of Technology
#    http://www.ait.ac.at
# 
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as
#    published by the Free Software Foundation, either version 2 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
# 
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/gpl-2.0.html


# Peter Kutschera, 2014-02-06
# Peter.Kutschera@ait.ac.at
#
# Register the OrionListener.py in PubSub

endpoint="http://crisma.ait.ac.at/orion"

(curl $endpoint/NGSI10/subscribeContext -s -S --header 'Content-Type: application/xml' -d @- | xmllint --format - | tee subscribeContext.xml) <<EOF
<?xml version="1.0"?>
<subscribeContextRequest>
  <entityIdList>
    <entityId type="WorldState" isPattern="true">
      <id>.*</id>
    </entityId>
  </entityIdList>
  <attributeList>
    <attribute>creation</attribute>
  </attributeList>
  <reference>http://crisma.ait.ac.at/indicators/OrionListener.py</reference>
  <duration>P3Y</duration>
  <notifyConditions>
    <notifyCondition>
      <type>ONCHANGE</type>
       <condValueList>
        <condValue>creation</condValue>
       </condValueList>
     </notifyCondition>
   </notifyConditions>
  <throttling>PT3S</throttling>
</subscribeContextRequest>
EOF
