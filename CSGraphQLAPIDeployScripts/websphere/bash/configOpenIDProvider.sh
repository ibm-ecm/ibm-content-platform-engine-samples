#/*
# IBM Confidential
# OCO Source Materials
# 5737-I23
# Copyright IBM Corp. 2021
# The source code for this program is not published or otherwise divested of its trade secrets, irrespective of what has been deposited with the U.S Copyright Office.
# */

#https://www.ibm.com/docs/en/was-liberty/base?topic=cocpil-configuring-openid-connect-provider-accept-client-registration-requests

#!/bin/bash

#uncomment for debugging
#set -x 

#uncomment set -e if want script to continue on error. Else, default to stop at 1st error
set -e


if [ "$1" != "" ]; then
	set -a 
	. "$1"
	set +a
fi
#env


#print out vars that is of array types to check if can be passed to UMS server
#echo "Redirect URIS = " "$OAUTH_REDIRECT_URIS"
#echo "Grant Types = " "$OAUTH_GRANT_TYPES"
#echo "Response Types = " "$OAUTH_RESPONSE_TYPES"

#Get a client
curl -X GET --header "Accept-Language:${acceptLanguage}" --header 'Content-Type:application/json' --header "Authorization: ${OAUTH_AUTHORIZATION_HEADER}" --header 'Accept:application/json' -w '\nReturn Code=%{http_code}\n\n' "${OAUTH_REGISTER_ENDPOINT}/${OAUTH_CLIENT_ID}" -k > tempfile.tmp
REST_STATUS_LINE=`grep "Return Code=" tempfile.tmp`
CLIENT_ID_LINE=`grep "client_id" tempfile.tmp`
#echo "REST status = " "$REST_STATUS_LINE"
#echo "Client Id = " "$CLIENT_ID_LINE"

#Client not found: 404
#Client found: 200
RET_CODE=`echo "$REST_STATUS_LINE" | sed 's/^Return Code=//g'`
#echo $RET_CODE
if [ "$RET_CODE" == "200" ]; then
	echo "GraphQL service is already registered. Update it"
	JSON_PUT_BODY="{
    \"client_secret_expires_at\": $OAUTH_CLIENT_SECRET_EXPIRES_AT, 
    \"token_endpoint_auth_method\": \""$OAUTH_TOKEN_ENDPOINT_AUTH_METHOD"\", 
    \"scope\": \""$OAUTH_SCOPE"\", 
    \"grant_types\": "$OAUTH_GRANT_TYPES", 
    \"response_types\": "$OAUTH_RESPONSE_TYPES",
    \"application_type\": \""$OAUTH_APPLICATION_TYPE"\", 
    \"post_logout_redirect_uris\": "$OAUTH_POST_LOGOUT_REDIRECT_URIS", 
    \"preauthorized_scope\": \""$OAUTH_PREAUTHORIZED_SCOPE"\", 
    \"introspect_tokens\": "$OAUTH_INTROSPECT_TOKENS", 
    \"trusted_uri_prefixes\": "$OAUTH_TRUSTED_URI_PREFIXES", 
    \"resource_ids\": "$OAUTH_RESOURCE_IDS", 
    \"functional_user_groupIds\": "$OAUTH_FUNCTIONAL_USER_GROUPIDS", 
    \"client_id\": \""$OAUTH_CLIENT_ID"\", 
    \"client_secret\": \""$OAUTH_CLIENT_SECRET"\", 
    \"client_name\": \""$OAUTH_CLIENT_NAME"\", 
    \"redirect_uris\": "$OAUTH_REDIRECT_URIS", 
    \"allow_regexp_redirects\": "$OAUTH_ALLOW_REGEXP_REDIRECTS"
}"
	#echo "JSON_PUT_BODY = " "$JSON_PUT_BODY"
	CMD="curl -X PUT --header 'Accept-Language:${acceptLanguage}' --header 'Content-Type:application/json' --header 'Authorization: ${OAUTH_AUTHORIZATION_HEADER}' --header 'Accept:application/json' -w '\nReturn Code=%{http_code}\n\n' ${OAUTH_REGISTER_ENDPOINT}/${OAUTH_CLIENT_ID} -k -d '$JSON_PUT_BODY' > tempfile.tmp"
	echo $CMD
	eval "$CMD"

	# check if return status = 200 (success). Else exit 1 since fail to register. 
	REST_STATUS_LINE=`grep "Return Code=" tempfile.tmp`
	RET_CODE=`echo "$REST_STATUS_LINE" | sed 's/^Return Code=//g'`
	if [ "$RET_CODE" != "200" ]; then
        	echo "Fail to update the registered client on UMS server. Check tempfile.tmp for error"
        	exit 1
	fi

elif [ "$RET_CODE" == "404" ]; then
	echo "GraphQL service has NOT been registered. Create it"
       JSON_POST_BODY="{
    \"client_secret_expires_at\": $OAUTH_CLIENT_SECRET_EXPIRES_AT,
    \"token_endpoint_auth_method\": \""$OAUTH_TOKEN_ENDPOINT_AUTH_METHOD"\",
    \"scope\": \""$OAUTH_SCOPE"\",
    \"grant_types\": "$OAUTH_GRANT_TYPES",
    \"response_types\": "$OAUTH_RESPONSE_TYPES",
    \"application_type\": \""$OAUTH_APPLICATION_TYPE"\",
    \"post_logout_redirect_uris\": "$OAUTH_POST_LOGOUT_REDIRECT_URIS",
    \"preauthorized_scope\": \""$OAUTH_PREAUTHORIZED_SCOPE"\",
    \"introspect_tokens\": "$OAUTH_INTROSPECT_TOKENS",
    \"trusted_uri_prefixes\": "$OAUTH_TRUSTED_URI_PREFIXES",
    \"resource_ids\": "$OAUTH_RESOURCE_IDS",
    \"functional_user_groupIds\": "$OAUTH_FUNCTIONAL_USER_GROUPIDS",
    \"client_id\": \""$OAUTH_CLIENT_ID"\",
    \"client_secret\": \""$OAUTH_CLIENT_SECRET"\",
    \"client_name\": \""$OAUTH_CLIENT_NAME"\",
    \"redirect_uris\": "$OAUTH_REDIRECT_URIS",
    \"allow_regexp_redirects\": "$OAUTH_ALLOW_REGEXP_REDIRECTS"
}"
        #echo "JSON_POST_BODY = " "$JSON_POST_BODY"
        CMD="curl -X POST --header 'Accept-Language:${acceptLanguage}' --header 'Content-Type:application/json' --header 'Authorization: ${OAUTH_AUTHORIZATION_HEADER}' --header 'Accept:application/json' -w '\nReturn Code=%{http_code}\n\n' ${OAUTH_REGISTER_ENDPOINT} -k -d '$JSON_POST_BODY' > tempfile.tmp"
        echo $CMD
	eval "$CMD"

	# check if return status = 201 (created ). Else exit 1 since fail to register. 
	REST_STATUS_LINE=`grep "Return Code=" tempfile.tmp`
	RET_CODE=`echo "$REST_STATUS_LINE" | sed 's/^Return Code=//g'`
	if [ "$RET_CODE" != "201" ]; then
        	echo "Fail to registered new client on UMS server. Check tempfile.tmp for error"
        	exit 1
	fi


else 
	echo "Fail to read registered clients on UMS server. Check tempfile.tmp for error"
	exit 1
fi
