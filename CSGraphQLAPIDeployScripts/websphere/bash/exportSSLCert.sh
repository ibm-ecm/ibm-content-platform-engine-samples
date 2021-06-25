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

#Exort CPE SSL certificate to a file
KEYTOOL_APP=$APPSERVER_BIN_DIR/../java/8.0/bin/keytool

cmd="$KEYTOOL_APP -export -keystore $APPSERVER_PROFILE_DIR/config/cells/$APPSERVER_CELL/nodes/$APPSERVER_NODE/key.p12 -storetype pkcs12 -storepass ${KEYSTOREPASS} -alias ${CPE_ALIAS} -file ${CPE_SELF_SIGNED_CERT} -noprompt"
result=$(eval "$cmd")
echo result