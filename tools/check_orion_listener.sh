#!/bin/bash
#

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
# Check registration of the OrionListener.py in PubSub

# note: as there is no method to do this I do an change subscription without any changes


endpoint="http://crisma.ait.ac.at/orion"

if [ -f subscribeContext.xml ]
    then

    (curl $endpoint/NGSI10/updateContextSubscription -s -S --header 'Content-Type: application/xml' -d @- | xmllint --format - ) <<EOF
<?xml version="1.0"?>
<updateContextSubscriptionRequest>
  $(grep "subscriptionId" subscribeContext.xml)
  <notifyConditions>
    <notifyCondition>
      <type>ONCHANGE</type>
      <condValueList>
        <condValue>creation</condValue>
      </condValueList>
    </notifyCondition>
  </notifyConditions>
</updateContextSubscriptionRequest>
EOF

fi
