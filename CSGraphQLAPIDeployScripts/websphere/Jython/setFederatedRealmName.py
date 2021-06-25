#/*
# IBM Confidential
# OCO Source Materials
# 5737-I23
# Copyright IBM Corp. 2021
# The source code for this program is not published or otherwise divested of its trade secrets, irrespective of what has been deposited with the U.S Copyright Office.
# */
#setFederatedRealmName.py
#https://www.ibm.com/docs/en/was/9.0.5?topic=scripting-securityrealminfocommands-command-group-admintask-object#rxml_7securityrealm__SecurityRealmInfoCommands.cmd5

import java


ldap_realm = sys.argv[0]

print "\nGet/Set realm name in Security/Global Security/Federated repositories/General Properties to: " + ldap_realm
defaultRealm = AdminTask.getIdMgrDefaultRealm()
if defaultRealm != ldap_realm:
        print "About to rename"
        print AdminTask.renameIdMgrRealm('[-name ' + defaultRealm + ' -newName ' + ldap_realm + ']')
	AdminConfig.save()
	# check again
	defaultRealm = AdminTask.getIdMgrDefaultRealm()
	if defaultRealm != ldap_realm :
		sys.exit("Fail to set federated realmName")
else:
        print "IdMgrDefaultRealm already has the correct value. No need to rename"



