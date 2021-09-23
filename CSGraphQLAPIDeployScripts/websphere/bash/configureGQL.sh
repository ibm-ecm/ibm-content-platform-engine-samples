#/*
# IBM Confidential
# OCO Source Materials
# 5737-I23
# Copyright IBM Corp. 2021
# The source code for this program is not published or otherwise divested of its trade secrets, irrespective of what has been deposited with the U.S Copyright Office.
# */
#!/bin/bash

# configureGQLsh

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

#set default if value is not set
if [[ "$GRAPHQL_APP_NAME" == "" ]]; then
	GRAPHQL_APP_NAME='content-services-graphql'
fi
if [[ "$IS_GRAPHQL_COLOCATE_WITH_CPE" == "" ]]; then
	IS_GRAPHQL_COLOCATE_WITH_CPE="false"
fi

#skip set up ldap and import CPE LTPA if IS_GRAPHQL_COLOCATE_WITH_CPE = false
#skip set SSO domain, inbound_realms_trusted since these values are from Global Security and should have been set by CPE
if [[ "$IS_GRAPHQL_COLOCATE_WITH_CPE" == "true" ]]; then
	echo "GraphQL is colocated with CPE, script will skip a number of operations"
	REQUIRE_LDAP_SETUP="false"
	LTPA_INTERMEDIATE_FILE=""
	SSO_DOMAIN=""
        INBOUND_REALMS_TRUSTED=""
        CPE_SELF_SIGNED_CERT=""
fi



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
       echo "#-----------------------"
       echo "#Restart Websphere server "
       echo "#-----------------------"
       date
       . ./restartWAS.sh
else
	echo "Skip setting up LDAP federated realm. "
fi



# extract this value from CPE appserver > Security > Global Security > Web and SIP Security > SSO > Domain Name
# since this value is stored in Global Security, if GraphQL and CPE is colocated in the same profile, skip this step
echo "#-----------------------"
echo "#enable SSO in GraphQLServer"
echo "#-----------------------"
date
if [[ $SSO_DOMAIN != "" ]]; then
	. ./enableSSO.sh
else
	echo "Skip enabling SSO since there is no SSO_DOMAIN specified."
fi


#extract LTPA file from CPE appserver > Security > Global Security > LTPA
#echo
#echo "#-----------------------"
#echo "# export LTPA from CEServer "
#echo "#-----------------------"
#date
#./exportLTPAKeys.sh  $LTPA_INTERMEDIATE_FILE $LTPA_PWD  # sanple only
#echo



echo
echo "#-----------------------"
echo "# import CEServer LTPAKeys from CEServer to GraphQL "
echo "#-----------------------"
date
if [[ "$LTPA_INTERMEDIATE_FILE" != "" ]] ; then
   if [[  $LTPA_PWD != "" ]]; then 
      . ./importLTPAKeys.sh  
   else
        echo "Missing defining value for LTPA_PWD"
   fi
else
   echo "Skip importing CPE LTPA "
fi

echo
echo "#-----------------------"
echo "# configure inbound trusted realms"
echo "#-----------------------"
if [[ $INBOUND_REALMS_TRUSTED != "" ]] ; then
	date
        . ./addTrustedRealm.sh
else
   echo "Skip configuring inbound trusted realms"
fi

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


#if CPE is colocated with GraphQL, assume that the Global Security > Application security > Enable application security is checked 
echo
echo
echo "#-----------------------"
echo "#enable Application Security in GraphQLServer"
echo "#-----------------------"
date
if [[ "$IS_GRAPHQL_COLOCATE_WITH_CPE" == "false" ]]; then
   . ./enableAppSecurity.sh
else
   echo "Skip enable Global Security > Application security "
fi

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
	echo "Skip importing CPE Self signed cert"
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



