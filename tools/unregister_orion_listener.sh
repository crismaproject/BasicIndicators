#!/bin/bash
#
# Peter Kutschera, 2014-02-06
# Peter.Kutschera@ait.ac.at
#
# Unregister the OrionListener.py in PubSub

endpoint="http://crisma.ait.ac.at/orion"

if [ -f subscribeContext.xml ]
    then

    (curl $endpoint/NGSI10/unsubscribeContext -s -S --header 'Content-Type: application/xml' -d @- | xmllint --format - ) <<EOF
<?xml version="1.0"?>
<unsubscribeContextRequest>
  <unsubscribeContext>
  $(grep "subscriptionId" subscribeContext.xml)
  </unsubscribeContext>
</unsubscribeContextRequest>
EOF
    
    rm subscribeContext.xml
fi
