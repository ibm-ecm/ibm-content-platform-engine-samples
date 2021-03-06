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

#TODO: make sure that JACE_JAR_FILE_PATH exists since Jython script does not care


$APPSERVER_BIN_DIR/wsadmin.sh -username $APPSERVER_WAS_USR -password $APPSERVER_WAS_PWD -conntype $APPSERVER_CONN_TYPE -f $JYTHON_DIR/createSharedLib.py $APPSERVER_CELL $APPSERVER_NODE $APPSERVER_SVR $JACE_JAR_FILE_PATH "$JACE_JAR_SYMBOLIC_NAME"

