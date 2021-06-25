#/*
# IBM Confidential
# OCO Source Materials
# 5737-I23
# Copyright IBM Corp. 2021
# The source code for this program is not published or otherwise divested of its trade secrets, irrespective of what has been deposited with the U.S Copyright Office.
# */
import java
#https://www.ibm.com/docs/en/was-zos/9.0.5?topic=domains-configuring-inbound-trusted-realms-multiple-security

#replace values for the following vars to match your env
realmsTrusted = sys.argv[0]
#end of replace values section. 

print AdminTask.listTrustedRealms('-communicationType inbound')
print AdminTask.addTrustedRealms('-communicationType inbound -realmList ' + realmsTrusted ) 

# Save config changes to master
AdminConfig.save()
