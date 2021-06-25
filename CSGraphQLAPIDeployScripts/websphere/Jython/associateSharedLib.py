#/*
# IBM Confidential
# OCO Source Materials
# 5737-I23
# Copyright IBM Corp. 2021
# The source code for this program is not published or otherwise divested of its trade secrets, irrespective of what has been deposited with the U.S Copyright Office.
# */
libName = sys.argv[0]
if (libName == ""):
	libName = 'CPE 557 Client Libs'
	print 'No libName passed in, default to ' + libName



library = AdminConfig.getid('/Library:" ' + libName + '"/')
print library

webModules = AdminConfig.list('WebModuleDeployment').split('\n')
for webModule in webModules:
        print webModule
        if (webModule.find("content-services-graphql") != -1):
            print 'Setting for ' + webModule
            classldr = AdminConfig.showAttribute(webModule, 'classloader')

            print AdminConfig.create('LibraryRef', classldr, [['libraryName', libName], ['sharedClassloader', 'true']])



AdminConfig.save()

