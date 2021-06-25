#/*
# IBM Confidential
# OCO Source Materials
# 5737-I23
# Copyright IBM Corp. 2021
# The source code for this program is not published or otherwise divested of its trade secrets, irrespective of what has been deposited with the U.S Copyright Office.
# */
if len(sys.argv)<4:
	print("argument should be cell node server jacejar-path")
	print("example: celll1 node1 server1 /tmp/Jace/jar")
	raise Exception("Invalid number of arguments")
cell1 = sys.argv[0]
node1 = sys.argv[1]
server1 = sys.argv[2]
sharedLib = sys.argv[3]
libName = sys.argv[4]


serv = AdminConfig.getid('/Cell:'+cell1+'/Node:'+node1+'/Server:'+server1)
print serv

AdminConfig.create('Library', serv, [['name', libName ], ['classPath', sharedLib]])
AdminConfig.save()

