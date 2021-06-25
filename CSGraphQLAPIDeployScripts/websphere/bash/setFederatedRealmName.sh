#/*
# IBM Confidential
# OCO Source Materials
# 5737-I23
# Copyright IBM Corp. 2021
# The source code for this program is not published or otherwise divested of its trade secrets, irrespective of what has been deposited with the U.S Copyright Office.
# */
#!/bin/bash

$APPSERVER_BIN_DIR/wsadmin.sh -username $APPSERVER_WAS_USR -password $APPSERVER_WAS_PWD -conntype $APPSERVER_CONN_TYPE -f $JYTHON_DIR/setFederatedRealmName.py $FEDERATED_REALM_NAME
