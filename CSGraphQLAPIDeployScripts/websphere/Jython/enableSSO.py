#/*
# IBM Confidential
# OCO Source Materials
# 5737-I23
# Copyright IBM Corp. 2021
# The source code for this program is not published or otherwise divested of its trade secrets, irrespective of what has been deposited with the U.S Copyright Office.
# */
import java

#replace values for the following vars to match your env
requiredSSL="true"
domainName=sys.argv[0]
#end of replace values section. 

# configure single sign on
print AdminTask.configureSingleSignon('[ -enable true -requiresSSL ' + requiredSSL + ' -domainName ' + domainName + 
			' -attributePropagation true ' + ' ]') 


# Save config changes to master
AdminConfig.save()
