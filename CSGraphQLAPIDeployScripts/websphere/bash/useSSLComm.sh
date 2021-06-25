#/* 
# IBM Confidential
# OCO Source Materials
# 5737-I23
# Copyright IBM Corp. 2021
# The source code for this program is not published or otherwise divested of its trade secrets, irrespective of what has been deposited with the U.S Copyright Office.
# */
#useSSLComm.sh
#Usage: useSSLComm.sh <properties_file>
#       This script will import the CPE SSL Certificate specified in CPE_SELF_SIGNED_CERT
#       to GraphQL trust store. It will then update the Jvm argument with value extracted
#       from CPE_URL
#!/bin/bash

#Uncomment for debugging
#set -x

#uncomment set -e if want script to continue on error. Else, default to stop at 1st error
set -e


if [ "$1" != "" ]; then
        set -a
        . "$1"
        set +a
fi

####
# Check required args
###
if [ "$APPSERVER_BIN_DIR" = "" ]
then
        echo "Need to set APPSERVER_BIN_DIR before running this script"
        exit 1
fi

#Import CPE SSL certificate into GraphQL tWAS server truststore
KEYTOOL_APP=$APPSERVER_BIN_DIR/../java/8.0/bin/keytool

cmd="$KEYTOOL_APP -importcert -keystore $APPSERVER_BIN_DIR/../profiles/AppSrv01/config/cells/$APPSERVER_CELL/nodes/$APPSERVER_NODE/trust.p12 -storetype pkcs12 -storepass ${KEYSTOREPASS} -alias ${CPE_ALIAS} -file ${CPE_SELF_SIGNED_CERT} -noprompt"
result=$(eval "$cmd")
echo result

echo ===================================================
echo Check that CPE_URL uses https endpoint
echo ===================================================
set -a
JVM_ARG_KEY="-Decm.content.remote.cpeuri"
if [[ "$CPE_URL" != *"https"* ]]
then
        echo "CPE_URL needs to use https endpoint in order to work with SSL."
        exit 1
fi
JVM_ARG_KEY_VALUE="$JVM_ARG_KEY=$CPE_URL"
echo $JVM_ARG_KEY_VALUE
set +a

$APPSERVER_BIN_DIR/wsadmin.sh -username $APPSERVER_WAS_USR -password $APPSERVER_WAS_PWD -conntype $APPSERVER_CONN_TYPE -f $JYTHON_DIR/addGenericJvmArg.py $APPSERVER_CELL $APPSERVER_NODE $APPSERVER_SVR $JVM_ARG_KEY $JVM_ARG_KEY_VALUE