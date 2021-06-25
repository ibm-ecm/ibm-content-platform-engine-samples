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

#Import CPE SSL certificate into GraphQL tWAS server truststore
KEYTOOL_APP=`find $APPSERVER_BIN_DIR/../ -name keytool`

echo "$KEYTOOL_APP -importcert -keystore $APPSERVER_PROFILE_DIR/config/cells/$APPSERVER_CELL/nodes/$APPSERVER_NODE/trust.p12 -storetype pkcs12 -storepass ${KEYSTOREPASS} -alias ${CPE_ALIAS} -file ${CPE_SELF_SIGNED_CERT}"

