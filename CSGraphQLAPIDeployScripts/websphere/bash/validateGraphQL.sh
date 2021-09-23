#/*
# IBM Confidential
# OCO Source Materials
# 5737-I23
# Copyright IBM Corp. 2021
# The source code for this program is not published or otherwise divested of its trade secrets, irrespective of what has been deposited with the U.S Copyright Office.
# */
#!/bin/bash
#set -x 

#uncomment set -e if want script to continue on error. Else, default to stop at 1st error
set -e


if [ "$1" != "" ]; then
	set -a 
	. "$1"
	set +a
fi

#ping and expect 'GOOD answer
PING_OUTPUT=`curl -X GET --header "Accept-Language:${acceptLanguage}" --header 'Content-Type:application/json' --header 'Accept:application/json' -w '\nReturn Code=%{http_code}\n\n' "${GraphQL_URL}/content-services/ping" | grep "Return Code"`

echo "Ping Output: " "$PING_OUTPUT"
if [[ "$PING_OUTPUT" == *"Return Code=200"* ]]; then
  echo "Successfully pinged GraphQL service"
  exit 0
else
  exit 1
fi
