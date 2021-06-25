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


#if is possible that server is already stopped, stop it again would fail
set +e 
$APPSERVER_BIN_DIR/stopServer.sh $APPSERVER_SVR -username $APPSERVER_WAS_USR -password $APPSERVER_WAS_PWD
set -e

$APPSERVER_BIN_DIR/startServer.sh $APPSERVER_SVR -username $APPSERVER_WAS_USR -password $APPSERVER_WAS_PWD 
