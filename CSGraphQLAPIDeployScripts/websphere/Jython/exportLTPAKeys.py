#/*
# IBM Confidential
# OCO Source Materials
# 5737-I23
# Copyright IBM Corp. 2021
# The source code for this program is not published or otherwise divested of its trade secrets, irrespective of what has been deposited with the U.S Copyright Office.
# */
import java

#replace values for the following vars to match your env
ltpaKeyFile= sys.argv[0]
password= sys.argv[1]
#end of replace values section. 

# import the ltpa key
AdminTask.exportLTPAKeys('[ -ltpaKeyFile file:' + ltpaKeyFile + ' -password ' + password + ']') 
