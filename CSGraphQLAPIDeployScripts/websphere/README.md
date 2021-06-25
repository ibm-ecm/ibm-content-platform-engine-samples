# Automating deployment of Content Services GraphQL API application on traditional WebSphere Application Server 9.0

## General Overview

This document describes how to run a Unix bash script to deploy the Content Services GraphQL (CSGQL) API application on a traditional Websphere Application Server (tWAS) 9.0 environment.

The limitations for this release are:

*   Scripts are written for the Linux/Unix platform only. If the traditional WebSphere Application Server (tWAS)  for hosting CSGQL is installed on Windows, follow the instructions described in the technical notice (technote) [Deploy Content Services GraphQL API into a traditional WebSphere Application Server environment](https://www.ibm.com/support/pages/node/6459811?_ga=2.146550964.1693779471.1624377485-1906706560.1624377485) to configure and deploy CSGQL manually.
*   Scripts target deployment under a tWAS single application server environment. 
*   Configuration of OAUTH is outside of the scope of these scripts. The scripts will configure GraphQL to use BASIC authentication with the Content Platform Engine (CPE) server. Information about OAUTH/OIDC configuration between CSGQL and CPE is provided in technical notice (technote) [Deploy Content Services GraphQL API into a traditional WebSphere Application Server environment](https://www.ibm.com/support/pages/node/6459811?_ga=2.146550964.1693779471.1624377485-1906706560.1624377485) .

After running the scripts, you will be able to make a Content Services GraphQL query to a CPE server and see the results of the query.

## Before you begin

To utilize these scripts, read and follow the procedures described in the technote. Pay special attention to all prerequisite items and preparation steps identified as being required prior to running the scripts.


## Bash scripts supplied

While many bash scripts are contained in this project, following are the ones you will interact with directly:

`configureGQL.sh --file <properties_file>`: this script will install GraphQL with Basic Authentication mode by default. If communications with the CPE will utilize SSL, several options exist:
*   Option 1: Manually export and transfer the CPE server's SSL certificate to the tWAS server hosting the CSGQL deployment as a part of the preparation. Update the properties file to include key-value pairs defined under the 'useSSLComm' section so GraphQL will be configured by the scripts to use SSL for communication.

*   Option 2: Set up GraphQL with Basic Authentication communication to CPE first without SSL certificate, and verify that GraphQL is working. Then update the properties file to include the path to the exported CPE SSL certificate and run the `useSSLComm.sh` script to perform the import of the certificate and configuration of CSGQL to use SSL for communication.

*   Option 3: Set up GraphQL with Basic Authentication communication to CPE first without SSL, verify that GraphQL is working. Then follow the manual instructions provided in the technote to import the CPE certificate and modify the CSGQL JVM argument to utilize SSL to connect to the `CPE_URL` https endpoint.

`useSSLComm.sh <properties_file>`: this script will import the CPE SSL certificate into GraphQL application server's trust store. It will then update the JVM argument to connect to the `CPE_URL` https endpoint.

`debugGQL.sh <properties_file>`: this script will enable or disable logging for GraphQL based on the setting of `ENABLE_GQL_DBG` and `ENABLE_LTPA_DBG`.

## What does the configureGQL.sh script do:

1.  The main bash script (configureGQL.sh) will read the environment variables defined in the input file (configureGQL.properties) and pass these environment variables to subscripts.
2.  Each subscript performs one specific task. Most tasks call tWAS wsadmin command line using a Jython subscript.  You can run subscript directly by passing in the same input file.
3.  All subscripts are run with the exception of those that create the federated repositories and LDAP servers configurations. These tasks can be controlled using the property `REQUIRE_LDAP_SETUP`. 
    *   Set to `false` if LDAP Federated is already set up (for example where CSGQL is installed in tWAS Network Deployment and CPE has already been installed previously or CSGQL is collocated in a tWAS instance where another application, IBM Content Navigator for example, has already set up the required configuration.) 
    *   Set to `true` and the subscripts are run to configure the federated repositories and LDAP servers in tWAS.

      
**The input files should be handled with care since they contain the user name, password, and secrets.  User should take appropriate measures to secure the input files.**

## How to run configureGQL.sh script:

1.  On the GraphQL server, make sure the tWAS has been installed and you can log in to tWAS console with valid credentials. You will need to edit the script input file and enter the information to access tWAS, including those credentials.  Additional information, such as the context where GraphQL will be installed, is also required as described below in the step about the [sample properties file](bash/configureGQL.properties.sample).
2.  Change to the CSGraphQLAPIDeployScripts folder that supports tWAS in your local repository previously cloned from this GitHub repository:
```
cd CSGraphQLAPIDeployScripts/websphere
```
3.  Navigate to the to the [bash directory](bash) in this project, then run the command `chmod a+x *.sh` to add the execute permissions to the shell scripts.
4.  A [sample properties file](bash/configureGQL.properties.sample) is provided in the [bash directory](bash). Make a copy of the sample property file and call it `<your_property_file>`. Update the values for keys in `<your_property_file>` using the comments in the file as your guide. For more information about how the inputs are utilized, refer to  [Deploy Content Services GraphQL API into a traditional WebSphere Application Server environment](https://www.ibm.com/support/pages/node/6459811?_ga=2.146550964.1693779471.1624377485-1906706560.1624377485)
5.  From the [bash directory](bash), run the command
```
./configureGQL.sh --file <your_property_file>
```
6.  After the scripts complete, access the content-services URL and enter a GraphQL query to verify the connection to the CPE server.

For example, to run the script with the `configureGQL.properties.<myenv>` file:  
```
./configureGQL.sh --file configureGQL.properties.<myenv>
```

Sample URL to get to GraphQL once deployed: [http://\<GraphQLHost\>:9080/content-services/](http://<GraphQLHost>:9080/content-services/)

Sample GraphQL query to test the connection to CPE:
```
{
  _apiInfo(repositoryIdentifier: "OS1")
  {
    buildDate
    implementationVersion
    buildNumber
    productVersion
    implementationTitle
    cpeInfo {
      cpeURL
      cpeUser
      repositoryName
    }
  }
}
```

## Completing the deployment:
After running the scripts, return to the [technote](https://www.ibm.com/support/pages/node/6459811?_ga=2.146550964.1693779471.1624377485-1906706560.1624377485) and complete the remainder of the procedures starting with the topic "Validate the Configuration". After usage of the Content Services GraphQL API is confirmed, OAuth/OIDC configuration between CS-GraphQL and CPE can be configured manually if desired.

Note the properties file can be modified to enable or disable logging for GraphQL based on the setting of `ENABLE_GQL_DBG` and `ENABLE_LTPA_DBG`. This script is then run to automate the setting of the trace flags if needed for troubleshooting an issue with the deployment.

```
debugGQL.sh <your_properties_file>
```
