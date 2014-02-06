#!/bin/bash
#
# Peter Kutschera, 2014-02-06
# Peter.Kutschera@ait.ac.at
#
# Emit an event simulationg a WorldState creation

endpoint="http://crisma.ait.ac.at/orion"
wsid=${1:-42}

t=$(date +%s)

echo "Update context ( set Attribute "creation") for WorldState $wsid to 'current_time': " $t

(curl $endpoint/NGSI10/updateContext -s -S --header 'Content-Type: application/xml' -d @- | xmllint --format - ) <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<updateContextRequest>
  <contextElementList>
    <contextElement>
      <entityId type="WorldState" isPattern="false">
        <id>$wsid</id>
      </entityId>
      <contextAttributeList>
        <contextAttribute>
          <name>creation</name>
          <type>creation</type>
          <contextValue>$t http://www.dilbert.com/</contextValue>
        </contextAttribute>
      </contextAttributeList>
    </contextElement>
  </contextElementList>
  <updateAction>APPEND</updateAction>
</updateContextRequest>
EOF

echo
echo Now check http://crisma.ait.ac.at/PubSub/PubSubContent.html if there is an indicator value.
echo Tip 1: Don\'t forget to klick \"Query Service\"
echo Tip 2: Search results for $t

