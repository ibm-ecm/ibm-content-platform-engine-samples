# IBM Content Platform Engine samples

## Scope

This repository contains various samples that can be used to extend Content Platform Engine.

## Sample projects
Here are a list of sample projects in this repository:
  - [**Content Event Webhook Receiver sample application**](ContentEventWebhookReceiver)
    - The Content Event Webhook Receiver sample application project contains code for creating a sample application that can be used as a Content Event Webhook Receiver. The application can be used as the base or inspiration for creating a custom Content Event Webhook Receiver application. The code for the sample application also contains examples of how to call the Content Services GraphQL API to retrieve data and make changes on a Content Platform Engine object store.
  - [**Content Services GraphQL API Schema**](CS-GraphQL-Schema)
      - The Content Services GraphQL API Schema project contains the GraphQL Schema file that defines the schema of the Content Services GraphQL API.
  - [**Content Services GraphQL API Deploy Scripts**](CSGraphQLAPIDeployScripts/websphere)
    - The Content Services GraphQL API Deploy Scripts project contains a set of instructions and scripts to help deploy the Content Services GraphQL API application on a traditional WebSphere Application Server.
  - [**Content Services GraphQL API Javascript Sample Application**](CS-GraphQL-javascript-samples)
    - The Content Services GraphQL API Javascript Sample Application contains a sample Javascript WebApplication to demonstrate basic communication with GraphQL API. This code demonstrates how to leverage GraphQL API to communicate and manipulate Content Platform Engine Object Store, and is intended for usage as inspiration and or base for custom applications.
  - [**Content Services Deployment API**](CS-Deployment-API)
    - The Content Services Deployment API project contains a sample that demonstrates usage of Jupyter Notebook to invoke Content Services Deployment API to deploy metadata such as Property Templates, Choices Lists, and Class Definitions across Content Platform Engine (CPE) Object Stores (OS) – export from source CPE domain/OS then import into destination CPE domain/OS.
  - [**Content Validation with ClamAV sample application**](ClamAVContentValidator)
    - The Content validation with ClamAV sample contains code for a content validator which utilises the ClamAV service to virus-check incoming content.
  - [**WAS CPE Must Gather Scripts**](MustGather)
    - The Content Platform Engine Must Gather scripts for WebSphere Application Server project contains scripts to help collect logs and other necessary debugging information from people using the WebSphere installation of FileNet Content Manager.
    
Note that the previously available **Content Services on Amazon Web Services sample applications** added in the [CPE 5.5.12 Release](https://github.com/ibm-ecm/ibm-content-platform-engine-samples/releases/tag/v5.5.12.0) have been removed, as those sample applications were specific for use with Content Services on Amazon Web Services.  The Content Services on Amazon Web Services offering has since been discontinued. However, the Content Platform Engine documentation has sample code to authenticate with an OAuth token. For that sample code, see [Single sign-on integrations via Content Engine API Bearer Token Authentication](https://www.ibm.com/docs/en/filenet-p8-platform/5.6.0?topic=authentication-single-sign-integrations-via-content-engine-api-bearer-token).

## License, Authors, and Change Log

If you would like to see the detailed LICENSE click [here](LICENSE).

If you would like to see the list of maintainers/authors for each sample click [here](MAINTAINERS.md).

If you would like to see the detailed list of changes on this repository [here](CHANGELOG.md).

```text
Licensed Materials - Property of IBM (c) Copyright IBM Corp. 2019,2025 All Rights Reserved.

US Government Users Restricted Rights - Use, duplication or disclosure restricted by GSA ADP Schedule Contract with
IBM Corp.

DISCLAIMER OF WARRANTIES :

Permission is granted to copy and modify this Sample code, and to distribute modified versions provided that both the
copyright notice, and this permission notice and warranty disclaimer appear in all copies and modified versions.

THIS SAMPLE CODE IS LICENSED TO YOU AS-IS. IBM AND ITS SUPPLIERS AND LICENSORS DISCLAIM ALL WARRANTIES, EITHER
EXPRESS OR IMPLIED, IN SUCH SAMPLE CODE, INCLUDING THE WARRANTY OF NON-INFRINGEMENT AND THE IMPLIED WARRANTIES OF
MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE. IN NO EVENT WILL IBM OR ITS LICENSORS OR SUPPLIERS BE LIABLE FOR
ANY DAMAGES ARISING OUT OF THE USE OF OR INABILITY TO USE THE SAMPLE CODE, DISTRIBUTION OF THE SAMPLE CODE, OR
COMBINATION OF THE SAMPLE CODE WITH ANY OTHER CODE. IN NO EVENT SHALL IBM OR ITS LICENSORS AND SUPPLIERS BE LIABLE
FOR ANY LOST REVENUE, LOST PROFITS OR DATA, OR FOR DIRECT, INDIRECT, SPECIAL, CONSEQUENTIAL, INCIDENTAL OR PUNITIVE
DAMAGES, HOWEVER CAUSED AND REGARDLESS OF THE THEORY OF LIABILITY, EVEN IF IBM OR ITS LICENSORS OR SUPPLIERS HAVE
BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
```
