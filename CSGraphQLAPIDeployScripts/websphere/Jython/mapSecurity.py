#/*
# IBM Confidential
# OCO Source Materials
# 5737-I23
# Copyright IBM Corp. 2021
# The source code for this program is not published or otherwise divested of its trade secrets, irrespective of what has been deposited with the U.S Copyright Office.
# */
print AdminApp.edit('content-services-graphql', '[-MapRolesToUsers [["AllAuthenticated" "no" "yes" "" "" "no" "" "" ]]]')
AdminConfig.save()

