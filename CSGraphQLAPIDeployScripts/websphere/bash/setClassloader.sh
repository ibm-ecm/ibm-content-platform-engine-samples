#/*
# IBM Confidential
# OCO Source Materials
# 5737-I23
# Copyright IBM Corp. 2021
# The source code for this program is not published or otherwise divested of its trade secrets, irrespective of what has been deposited with the U.S Copyright Office.
# */
#!/bin/bash

#uncomment set -e if want script to continue on error. Else, default to stop at 1st error
set -e



if [ "$1" != "" ]; then
	set -a 
	. "$1"
	set +a
fi

#set default if value is not set
if [[ '$GRAPHQL_APP_NAME' == "" ]]; then
	GRAPHQL_APP_NAME='content-services-graphql'
fi

$APPSERVER_BIN_DIR/wsadmin.sh -username $APPSERVER_WAS_USR -password $APPSERVER_WAS_PWD -conntype $APPSERVER_CONN_TYPE -f $JYTHON_DIR/setClassloader.py $GRAPHQL_APP_NAME
