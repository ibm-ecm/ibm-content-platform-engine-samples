#/*
# IBM Confidential
# OCO Source Materials
# 5737-I23
# Copyright IBM Corp. 2021
# The source code for this program is not published or otherwise divested of its trade secrets, irrespective of what has been deposited with the U.S Copyright Office.
# */
#!/bin/bash

#uncomment following line for debug mode
#set -x

#uncomment set -e if want script to continue on error. Else, default to stop at 1st error
set -e


#import env vars from file passed in via $1
if [ "$1" != "" ]; then
	set -a 
	. "$1"
	set +a
fi

#make sure that JYTHON_DIR is defined
if [[ ! -d "$JYTHON_DIR" ]]; then
	echo "Please set JYTHON_DIR to the directory where wsadnin scripts are downloaded and rerun this program."
	exit 1
fi

#TODO can do all sort of args check if want to
#




echo "set _wasVersion \"${WASVERSION}\"" > $JYTHON_DIR/configureWSLDAPFederated.tcl_runtime
echo "set _admConsoleUser \"${WASADMIN}\"" >> $JYTHON_DIR/configureWSLDAPFederated.tcl_runtime
echo "set _setCurrent \"${SETCURRENT}\"" >> $JYTHON_DIR/configureWSLDAPFederated.tcl_runtime
echo "set _ldapType \"${LDAPTYPE}\"" >> $JYTHON_DIR/configureWSLDAPFederated.tcl_runtime
echo "set _ldapServerHost \"${LDAP_SVR}\"" >> $JYTHON_DIR/configureWSLDAPFederated.tcl_runtime
echo "set _ldapServerPort \"${LDAP_PORT}\"" >> $JYTHON_DIR/configureWSLDAPFederated.tcl_runtime
echo "set _sslEnabled \"${LDAP_ENABLE_SSL}\"" >> $JYTHON_DIR/configureWSLDAPFederated.tcl_runtime
echo "set _ldapBindDN \"${LDAP_BIND_DN}\"" >> $JYTHON_DIR/configureWSLDAPFederated.tcl_runtime
echo "set _bindPassword \"${LDAP_BIND_PWD}\"" >> $JYTHON_DIR/configureWSLDAPFederated.tcl_runtime
echo "set _baseEntryNDRealm \"${LDAP_BASE}\"" >> $JYTHON_DIR/configureWSLDAPFederated.tcl_runtime
echo "set _baseEntryNDRepository \"${LDAP_BASE_REPO}\"" >> $JYTHON_DIR/configureWSLDAPFederated.tcl_runtime
echo "set _repoId \"${REPO_ID}\"" >> $JYTHON_DIR/configureWSLDAPFederated.tcl_runtime
echo "set _loginProperties \"$LDAP_LOGIN_PROP\"" >> $JYTHON_DIR/configureWSLDAPFederated.tcl_runtime
echo "set _fedReposRealm \"$LDAP_FED_REALM\"" >> $JYTHON_DIR/configureWSLDAPFederated.tcl_runtime
echo "set _groupMembershipName \"$LDAP_GROUP_MEMBERSHIP_ATTR\"" >> $JYTHON_DIR/configureWSLDAPFederated.tcl_runtime
echo "set _groupMembershipScope \"$LDAP_GROUP_MEMBERSHIP_SCOPE\"" >> $JYTHON_DIR/configureWSLDAPFederated.tcl_runtime
echo "set _domainNotSet \"$LDAP_DOMAIN_NOT_SET\"" >> $JYTHON_DIR/configureWSLDAPFederated.tcl_runtime
echo "set _turnoffSSLcerts \"$LDAP_TURNOFF_SSL_CERTS\"" >> $JYTHON_DIR/configureWSLDAPFederated.tcl_runtime
more $JYTHON_DIR/configureWSLDAPFederated.tcl >> $JYTHON_DIR/configureWSLDAPFederated.tcl_runtime

$APPSERVER_BIN_DIR/wsadmin.sh -username $APPSERVER_WAS_USR -password $APPSERVER_WAS_PWD -conntype $APPSERVER_CONN_TYPE -f $JYTHON_DIR/configureWSLDAPFederated.tcl_runtime -lang jacl
rm $JYTHON_DIR/configureWSLDAPFederated.tcl_runtime 

