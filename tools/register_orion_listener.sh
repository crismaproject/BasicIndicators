#!/bin/bash
#
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
