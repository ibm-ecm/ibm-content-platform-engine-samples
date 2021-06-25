#/*
# IBM Confidential
# OCO Source Materials
# 5737-I23
# Copyright IBM Corp. 2021
# The source code for this program is not published or otherwise divested of its trade secrets, irrespective of what has been deposited with the U.S Copyright Office.
# */
#enableAppSecurity.py
#https://www.ibm.com/docs/en/was/9.0.5?topic=scripting-securityconfigurationcommands-command-group-admintask-object

import java

print ("BEFORE enable app security ")
print AdminTask.getCurrentWizardSettings ()


# enable application security
AdminTask.setAdminActiveSecuritySettings ('[-appSecurityEnabled true]')

# Save config changes to master
AdminConfig.save()

checkAppSecEnable = AdminTask.isAppSecurityEnabled()
if checkAppSecEnable != "true":
	print("Fail to enable application security")
	raise Exception("Fail to enable application security")
else:
	print ("1AFTER enable app security ")
	print AdminTask.getCurrentWizardSettings ()
