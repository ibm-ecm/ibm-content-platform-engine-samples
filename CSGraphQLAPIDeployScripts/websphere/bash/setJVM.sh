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

$APPSERVER_BIN_DIR/wsadmin.sh -username $APPSERVER_WAS_USR -password $APPSERVER_WAS_PWD -conntype $APPSERVER_CONN_TYPE -f $JYTHON_DIR/setJVM.py $APPSERVER_CELL $APPSERVER_NODE $APPSERVER_SVR $CPE_URL $APPEND_JVM  $ECM_CONTENT_GRAPHQL_CORS_ORIGIN_URL

#JVM requires a restart for the arguments to take effect. 
#For required restart, see https://www.ibm.com/support/pages/setting-generic-jvm-arguments-websphere-application-server
. $SCRIPT_DIR/restartWAS.sh 