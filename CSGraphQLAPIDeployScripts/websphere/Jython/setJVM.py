#/*
# IBM Confidential
# OCO Source Materials
# 5737-I23
# Copyright IBM Corp. 2021
# The source code for this program is not published or otherwise divested of its trade secrets, irrespective of what has been deposited with the U.S Copyright Office.
# */
mycell = sys.argv[0]
mynode = sys.argv[1]
server1= sys.argv[2]
cpeurl = sys.argv[3]
appendJVM = sys.argv[4]
ECM_CONTENT_GRAPHQL_CORS_ORIGIN_URL= sys.argv[5]

server1 = AdminConfig.getid('/Cell:'+mycell+'/Node:'+mynode+'/Server:'+server1+'/')
print server1

jvm_id=AdminConfig.list('JavaVirtualMachine',server1)
print jvm_id

current_arguments=AdminConfig.showAttribute(jvm_id,"genericJvmArguments")
#print str(current_arguments)

if (appendJVM == 'true'):
    new_arguments = current_arguments+' '+'-Dmetadata.cache.refresh.interval=120'
else:
    new_arguments = '-Dmetadata.cache.refresh.interval=120'

new_arguments = new_arguments+' '+'-Dcom.ibm.ecm.content.graphql.enable.graphiql=TRUE'

new_arguments = new_arguments+' '+'-Dcom.ibm.ws.http.options.writeTimeout=180'
new_arguments = new_arguments+' '+'-Dcom.ibm.ws.http.options.readTimeout=180'


new_arguments = new_arguments+' '+'-Dhttps.protocols=TLSv1.2'
new_arguments = new_arguments+' '+'-Dcom.filenet.authentication.wsi.AuthTokenOrder=oauth,ltpa'
new_arguments = new_arguments+' '+'-DFileNet.WSI.AutoDetectLTPAToken=true'
new_arguments = new_arguments+' '+'-Dcom.filenet.authentication.wsi.AutoDetectAuthToken=true'
new_arguments = new_arguments+' '+'-Dsun.net.http.retryPost=false'

new_arguments = new_arguments+' '+'-Decm.content.remote.cpeuri='+cpeurl

# args for CORS Cross-Origin Resource Sharing. (CORS)is an HTTP-header based mechanism 
# that allows a server to indicate any other origins (domain, scheme, or port) than its own 
# from which a browser should permit loading of resources.
new_arguments = new_arguments+' '+'-Decm.content.graphql.cors.enable=true'

#CORS JVM 
new_arguments = new_arguments+' '+'-Decm.content.graphql.cors.origin.url=' + ECM_CONTENT_GRAPHQL_CORS_ORIGIN_URL
new_arguments = new_arguments+' '+'-Decm.content.graphql.cors.allow.methods=GET,POST,OPTIONS,PUT,DELETE,HEAD'
new_arguments = new_arguments+' '+'-Decm.content.graphql.cors.allow.credentials.boolean=true'
new_arguments = new_arguments+' '+'-Decm.content.graphql.cors.allow.headers='\
                'Connection, Pragma, Cache-Control, Navigator-Client-Build, XSRFtoken, '\
                'Origin, User-Agent, Content-Type, Content-Length, Navigator-Client-Identity, '\
                'Accept-Control-Request-Method, Accept-Control-Request-Headers, Accept, Referer, '\
                'Accept-Encoding, Accept-Language, DNT, Host, Content-Length, Cache-control, Cookie'
new_arguments = new_arguments+' '+'-Decm.content.graphql.cors.max.age.seconds=86400'
#done with CORS JVM

print AdminConfig.modify(jvm_id,[['genericJvmArguments', new_arguments]])
AdminConfig.save()

current_arguments=AdminConfig.showAttribute(jvm_id,"genericJvmArguments")
print 'JVM post UPDATE = ' 
print str(current_arguments)

