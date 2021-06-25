#/*
# IBM Confidential
# OCO Source Materials
# 5737-I23
# Copyright IBM Corp. 2021
# The source code for this program is not published or otherwise divested of its trade secrets, irrespective of what has been deposited with the U.S Copyright Office.
# */
#See: https://www.ibm.com/docs/en/was-zos/8.5.5?topic=caus-modifying-war-class-loader-mode-using-wsadmin-scripting
#See: http://setgetweb.com/p/WAS85x/ae/rxml_7libserver.html

myApplication='content-services-graphql'

#Set a reference to the deployment.xml document
deployments = AdminConfig.getid('/Deployment:content-services-graphql/')
print "deployments of GraphQL: " + deployments
print

mode1 = 'PARENT_LAST'

#Set a reference to the deployedObject attribute within the deployment.xml document and set it to the deployedObject variable.
deploymentObject = AdminConfig.showAttribute(deployments, 'deployedObject')


classLoader = AdminConfig.showAttribute(deploymentObject, 'classloader')
print classLoader
print "modify classLoader mode to " + mode1 + AdminConfig.modify(classLoader, [['mode', mode1]])
print "verify modification: " + AdminConfig.showall(classLoader)

#List the modules for the deployedObject attribute and set the list to the myModules variable.
myModules = AdminConfig.showAttribute(deploymentObject, 'modules')
print "Expect to see graphQL" + myModules
myModules = myModules[1:len(myModules)-1].split(" ")
print myModules

#Find the web module and set the mode for the class loader.
for module in myModules:
     if (module.find('content-services-graphql')!= -1):
        AdminConfig.modify(module, [['classloaderMode', mode1]])
AdminConfig.save()
print "verify modification: " + AdminConfig.showall(classLoader) 

#Verify the changes that you made to the attribute value with the showall command.
for module in myModules:
     if (module.find('content-services-graphql')!= -1):
        print AdminConfig.showall(module)

#change WAR class loader policy from 'Class loader for each WAR file in application' to 'Single class loader for application'
warClassLoader = AdminConfig.showAttribute(deploymentObject, 'warClassLoaderPolicy')
print "war classLoader policy BEFORE modification: " + warClassLoader
print "modify war ClassLoader policy to " + "SINGLE" + AdminConfig.modify(deploymentObject , [['warClassLoaderPolicy', 'SINGLE']])
AdminConfig.save()
print "verify war classLoader policy AFTER modification: " + AdminConfig.show (deploymentObject, 'warClassLoaderPolicy' )


