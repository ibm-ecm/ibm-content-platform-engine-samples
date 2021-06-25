#/*
# IBM Confidential
# OCO Source Materials
# 5737-I23
# Copyright IBM Corp. 2021
# The source code for this program is not published or otherwise divested of its trade secrets, irrespective of what has been deposited with the U.S Copyright Office.
# */
#debugGQL.sh
#Usage: debugGQL.sh <properties_file>
#    Enable or disable GraphQL / LTPA debugging depends on setting of 
#    ENABLE_GQL_DBG and ENABLE_LTPA_DBG env vars

#!/bin/bash

#uncomment set -e if want script to continue on error. Else, default to stop at 1st error
set -e


if [ "$1" != "" ]; then
	set -a 
	. "$1"
	set +a
fi


$APPSERVER_BIN_DIR/wsadmin.sh -username $APPSERVER_WAS_USR -password $APPSERVER_WAS_PWD -conntype $APPSERVER_CONN_TYPE -f $JYTHON_DIR/debugGQL.py $ENABLE_GQL_DBG $ENABLE_LTPA_DBG $APPSERVER_CELL $APPSERVER_NODE $APPSERVER_SVR

