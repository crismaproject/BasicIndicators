#!/bin/bash
#
# Peter Kutschera, Thu Feb  6 12:42:00 2014
# Time-stamp: "2014-02-07 08:14:37 peter"

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

