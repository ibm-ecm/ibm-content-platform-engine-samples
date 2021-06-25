#/*
# IBM Confidential
# OCO Source Materials
# 5737-I23
# Copyright IBM Corp. 2021
# The source code for this program is not published or otherwise divested of its trade secrets, irrespective of what has been deposited with the U.S Copyright Office.
# */
#!/bin/bash

#set -x

#uncomment set -e if want script to continue on error. Else, default to stop at 1st error
set -e


#-----------------------------------------------------
######### Functions
#-----------------------------------------------------
f_usage()
{
    echo "NAME"
    echo "  $0 -- deploy and configure GraphQL application on traditional Websphere . "
    echo ""
    echo "USAGE: $0  "
    echo "    [--file               inputFile to store Key/Value pair for arguments]"
    echo "    [-h]"
    echo ""
    echo "EXAMPLES:"
    echo "$0 "
    echo "   --file configureGraphQL.properties "
}

f_extractFieldsFromFile()
{
        echo 'Extracting fields from file' $INPUT_FILE ......
	set -a 
	. ./$INPUT_FILE
	set +a
	env
}

#-----------------------------------------------------
####### Main
#-----------------------------------------------------
#parse arg
while [ "$1" != "" ]; do
    case $1 in
        --file)                 shift
                                                                INPUT_FILE="$1"
                                                                f_extractFieldsFromFile
                                                                ;;
        -h)                     f_usage
                                exit 1
    esac
    shift
done


if [ "$APPSERVER_BIN_DIR" == "" ]; then
	echo "APPSERVER_BIN_DIR var is required. Either set it by pass in --file <properties_file> or set shell vars before running."
	exit 1
fi

echo "#-----------------------"
echo "#Restart Websphere server "
echo "#-----------------------"
date
. ./restartWAS.sh


echo "#-----------------------"
echo "#configure Federated LDAP "
echo "#-----------------------"
date
if [[ "$REQUIRE_LDAP_SETUP" == "true" ]]; then
	. ./configureWSLDAPFederated.sh 
else
	echo "Skip setting up LDAP federated realm. "
fi


echo "#-----------------------"
echo "#Restart Websphere server "
echo "#-----------------------"
date
. ./restartWAS.sh


echo "#-----------------------"
echo "#enable SSO in GraphQLServer"
echo "#-----------------------"
date
if [[ $SSO_DOMAIN != "" ]]; then
	. ./enableSSO.sh
else
	echo "Skip enabling SSO since there is no SSO_DOMAIN specified."
fi


#echo
#echo "#-----------------------"
#echo "# export LTPA from CEServer "
#echo "#-----------------------"
if [[ $LTPA_INTERMEDIATE_FILE == "" || $LTPA_PWD == "" ]]; then
	echo "Missing defining keys for LTPAImport"
	exit 1
fi
#date
#./exportLTPAKeys.sh  $LTPA_INTERMEDIATE_FILE $LTPA_PWD  # sanple only
#echo



echo
echo "#-----------------------"
echo "# import CEServer LTPAKeys from CEServer to GraphQL"
echo "#-----------------------"
date
. ./importLTPAKeys.sh  


echo
echo "#-----------------------"
echo "# configure inbound trusted realms"
echo "#-----------------------"
if [[ $INBOUND_REALMS_TRUSTED == "" ]]; then
	echo "Missing defining keys for addTrustedRealm"
	exit 1
fi
date
. ./addTrustedRealm.sh

echo
echo "#-----------------------"
echo "# deploy Content Services GraphQL"
echo "# set Context Root"
echo "#-----------------------"
date
if [[ $CONTENT_GRAPH_API_WAR_PATH = "" ]]; then
	echo "Missing defining keys for install"
	exit 1
fi
. ./install.sh


echo
echo "#-----------------------"
echo "# create shared libraries"
echo "#-----------------------"
date
. ./createSharedLib.sh


echo
echo "#-----------------------"
echo "# associate shared libraries with GraphQL application"
echo "#-----------------------"
date
#use params in create shared libraries
. ./associateSharedLib.sh


echo
echo "#-----------------------"
echo "# set the parentlast class loader policy"
echo "#-----------------------"
date
. ./setClassloader.sh

echo 
echo "#-----------------------"
echo "# map application security to all authenticated"
echo "#-----------------------"
date
. ./mapSecurity.sh

echo
echo
echo "#-----------------------"
echo "#enable Application Security in GraphQLServer"
echo "#-----------------------"
date
. ./enableAppSecurity.sh

echo 
echo "#-----------------------"
echo "# set JVM args"
echo "#-----------------------"
date
. ./setJVM.sh

if [[ $CPE_SELF_SIGNED_CERT != "" ]]; then
	echo
	echo "#-----------------------"
	echo "#import CPE Self signed certficate"
	echo "#-----------------------"
	date
	. ./useSSLComm.sh 
else
	echo "Skip importing CPE Self signed cert since no CPE_SELF_SIGNED_CERT is specified"
fi


if [[ $ENABLE_GQL_DBG == "true" || $ENABLE_LTPA_DBG == "true" ]]; then
	echo 
	echo "#-----------------------"
	echo "# enable Debugging "
	echo "#-----------------------"
	date
	. ./debugGQL.sh
fi 

echo 
echo "#-----------------------"
echo "# restart CS-GraphQL tWAS"
echo "#-----------------------"
date
. ./restartWAS.sh


echo
echo "#-----------------------"
echo "#Validate the configuration by pinging CS-GraphQL using Basic auth"
echo "#-----------------------"
date
. ./validateGraphQL.sh




#echo
#echo "#-----------------------"
#echo "# Oauth/OIDC set up between CS-GraphQL and CPE"
#echo "#-----------------------"
#date
#. ./configOpenIDProvider.sh



