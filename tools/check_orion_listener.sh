#!/bin/bash
#
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
