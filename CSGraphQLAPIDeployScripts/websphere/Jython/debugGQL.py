#/*
# IBM Confidential
# OCO Source Materials
# 5737-I23
# Copyright IBM Corp. 2021
# The source code for this program is not published or otherwise divested of its trade secrets, irrespective of what has been deposited with the U.S Copyright Office.
# */
#AdminConfig: https://www.ibm.com/docs/en/bpm/8.5.6?topic=levels-changing-log-details-wsadmin

enableGQLTrace = sys.argv[0]
enableLTPATrace = sys.argv[1]
mycell = sys.argv[2]
mynode = sys.argv[3]
server1 = sys.argv[4]

GQLComponent = 'com.ibm.ecm.content.graphql.*=all'
LTPAComponent = 'com.ibm.ws.security.ltpa.LTPAToken2=all'

###### Configure trace
#identify the server that is being traced
server1 = AdminConfig.getid('/Cell:'+mycell+'/Node:'+mynode+'/Server:'+server1+'/')
print 'server: ' + server1

#identify the trace service for this appserver
tc=AdminConfig.list('TraceService',server1)
print 'current tc: ' + tc


if (enableGQLTrace == 'true'):
    traceSpec = GQLComponent + '=enabled'
else:
    traceSpec = GQLComponent + '=disabled'

if (enableLTPATrace == 'true'):
    traceSpec = traceSpec + ':' + LTPAComponent + '=enabled'
else:
    traceSpec = GQLComponent + '=disabled'
AdminConfig.modify(tc, [['startupTraceSpecification',  traceSpec]])
AdminConfig.save()


#TODO:
#Correlation: https://www.ibm.com/docs/en/was-nd/9.0.5?topic=applications-configuring-xct-wsadmin-scripting

AdminConfig.save()
