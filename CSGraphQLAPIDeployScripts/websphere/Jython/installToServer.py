#/* 
# IBM Confidential
# OCO Source Materials
# 5737-I23
# Copyright IBM Corp. 2021
# The source code for this program is not published or otherwise divested of its trade secrets, irrespective of what has been deposited with the U.S Copyright Office.
# */

#https://www.ibm.com/docs/he/was-nd/8.5.5?topic=scripting-installing-enterprise-applications-using-wsadmin

#print the current list of applications installed
appsInstalled = AdminApp.list()
print "applications installed: " + appsInstalled

appName = sys.argv[0]
filename = sys.argv[1]
updatewar = sys.argv[2]


index = appsInstalled.find (appName)
print "GraphQL installed at index (-1 means never installed): " + str(index)

#check if want to install on cluster or server
if len(sys.argv) == 4:
                        clusterName = sys.argv[3]
                        print "========================================================================"
                        print "Installing " + filename + " on cluster = " + clusterName +  "..."
                        print "========================================================================"
                        if (index == -1 ):
                        	print ("GraphQL has not been installed on this cluster . Go and install it on the cluster")
                        	AdminApp.install(filename, ['-cluster', clusterName, '-appname', appName, '-MapWebModToVH', [['.*', '.*', 'default_host']], '-CtxRootForWebMod', [['content-graphql-api.war', 'content-graphql-api.war,WEB-INF/web.xml', '/content-services']]])
                        elif (updatewar == "true"):
                        	print ("Update existing installed GraphQL")
                        	AdminApp.install(filename, ['-update', '-cluster', clusterName, '-appname', appName, '-MapWebModToVH', [['.*', '.*', 'default_host']], '-CtxRootForWebMod', [['content-graphql-api.war', 'content-graphql-api.war,WEB-INF/web.xml', '/content-services']]])
                        else:
                            raise Exception ("Exit since user does not want to overwrite the current GraphQL installation.")
                        AdminConfig.save()


elif len(sys.argv) == 5:
                        node1 = sys.argv[3]
                        server1 = sys.argv[4]
                        print "========================================================================"
                        print "Installing " + filename + " on node:server = " + node1 + ":" + server1 + "..."
                        print "========================================================================"
                        if (index == -1 ):
                            print ("First time installed GraphQL")
                            AdminApp.install(filename, ['-node', node1, '-server', server1, '-appname', appName, '-MapWebModToVH', [['content-graphql-api.war', 'content-graphql-api.war,WEB-INF/web.xml', 'default_host']], '-CtxRootForWebMod', [['content-graphql-api.war', 'content-graphql-api.war,WEB-INF/web.xml', '/content-services']]])
                        elif (updatewar == "true"):
                           print ("Update existing installed GraphQL")
                           AdminApp.install(filename, ['-update', '-node', node1, '-server', server1, '-appname', appName, '-MapWebModToVH', [['content-graphql-api.war', 'content-graphql-api.war,WEB-INF/web.xml', 'default_host']], '-CtxRootForWebMod', [['content-graphql-api.war', 'content-graphql-api.war,WEB-INF/web.xml', '/content-services']]])
                        else:
                            raise Exception ("Exit since user does not want to overwrite the current GraphQL installation.")
                        AdminConfig.save()

else:
                        print("Invalid number of arguments\n")
                        raise Exception("Invalid number of arguments")
