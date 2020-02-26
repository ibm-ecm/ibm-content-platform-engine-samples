# Content Event Webhook Receiver sample application
This folder contains code for creating a sample application that can be used as a Content Event Webhook Receiver. The application can be used as the base or inspiration for creating a custom Content Event Webhook Receiver application. The code for the sample application also contains examples of how to call the Content Services GraphQL API to retrieve data and make changes on a Content Platform Engine object store.

For more information about Content Event Webhooks, see the developer guide topic [(V5.5.4 and later) Content Platform Engine event webhooks](https://www.ibm.com/support/knowledgecenter/en/SSNW2F_5.5.0/com.ibm.p8.ce.dev.ce.doc/webhooks_concepts.htm).

---
### Preparing the Content Platform Engine object store
Before using the Webhook Receiver sample application, you will need to prepare an object store on the Content Platform Engine server:

- Install the **5.5.4 Event-Driven External Service Invocation Extensions** add-on on the object store you will associate with the webhook. For more information on how to do this, see the topic [Installing an add-on feature to an object store](https://www.ibm.com/support/knowledgecenter/en/SSNW2F_5.5.0/com.ibm.p8.ce.admin.tasks.doc/featureaddons/fa_install_addon.htm).
- Import the [WebhookClaim.zip](files/WebhookClaim.zip) deployment package (located in the [`files`](files) subdirectory) into the the object store you will associate with the webhook. Alternatively, you can manually create the *WebhookClaim* document class as described in section [**Details about the Webhook Receiver sample application**](#details-about-the-webhook-receiver-sample-application). To import the WebhookClaim deployment package, see the topic [Deploying assets with FileNet Deployment Manager](https://www.ibm.com/support/knowledgecenter/en/SSNW2F_5.5.0/com.ibm.p8.common.deploy.doc/p8pdb020.htm). The following high level steps show the process for deploying the package:
    1. Create an environment definition to use as the source by expanding the WebhookClaim deployment package. See the topic [Create or edit an environment definition from a deployment package](https://www.ibm.com/support/knowledgecenter/en/SSNW2F_5.5.0/com.ibm.p8.common.deploy.doc/p8pdb038.htm).
    2. Create a destination environment definition, which you will use to import the WebhookClaim document class into the object store that is associated with the webhook. [Create environment definitions](https://www.ibm.com/support/knowledgecenter/en/SSNW2F_5.5.0/com.ibm.p8.common.deploy.doc/deploy_mgr_checklist_environ_def.htm).
    3. Create a source-destination pair definition to handle mapping, converting, and importing the WebhookClaim document class. See the topic [Create a source-destination pair definition](https://www.ibm.com/support/knowledgecenter/en/SSNW2F_5.5.0/com.ibm.p8.common.deploy.doc/deploy_mgr_checklist_pair_def.htm). Map the source object store *Daph1* to the object store you will associate with the webhook. Map the user *ceadmin* and group *ceadmingroup* to principals that have **Full Control** access on the object store.
    4. Convert and import the WebhookClaim deployment data set. See the topics [Converting objects for import](https://www.ibm.com/support/knowledgecenter/en/SSNW2F_5.5.0/com.ibm.p8.common.deploy.doc/prep_data_ce_convert_objects.htm) and [Importing converted objects](https://www.ibm.com/support/knowledgecenter/en/SSNW2F_5.5.0/com.ibm.p8.common.deploy.doc/deploy_ce_import_objects.htm).
        - When you import the WebhookClaim deployment data set and specify your import options per the topic [Configuring an import options set file](https://www.ibm.com/support/knowledgecenter/en/SSNW2F_5.5.0/com.ibm.p8.common.deploy.doc/deploy_ce_import_options_set_file.htm)), uncheck the options **Import Security Permissions**, **Import Owner**, and **Use Original Create/Update Timestamps and Users**. Use the default values for all other options.
        - Unchecking these options means that most of the security mapping is ignored. However, the Access Permisions on the **Default Instance Security** for the WebhookClaim document class must still be mapped.
        - After importing the WebhookClaim deploy dataset, review the **Default Instance Security** for the imported WebhookClaim (display name **Claim**) document class. See the topic [Add users and groups to a class](https://www.ibm.com/support/knowledgecenter/en/SSNW2F_5.5.0/com.ibm.p8.security.doc/p8psh003.htm). Modify the access permissions as desired.

---
### Preparing the Webhook Receiver sample application development environment

This project uses the [Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html) to download a Gradle distribution to execute its build. The Gradle distribution can be used to set up a development environment for Eclipse. 
To generate the files that are required to import this project into Eclipse (`File - Import…​ - Existing Projects into Workspace`), run the following Gradle task:

- **Windows**: `gradlew.bat eclipse`
- **Linux/Mac**: `./gradlew eclipse`

A `.project` and `.classpath` file are generated in the root of the project.

If you want to later change the dependencies, for example, because you are making modifications to the sample application, you must run the following Gradle command to refresh your Eclipse classpath:

- **Windows**: `gradlew.bat --refresh-dependencies eclipseClasspath`
- **Linux/Mac**: `./gradlew --refresh-dependencies eclipseClasspath`

A new `.classpath` file is generated. Then, in Eclipse, right click on the Project and select Refresh to reload the `.classpath` file.

---
### Details about the Webhook Receiver sample application

The Webhook Receiver sample application is used to demonstrate both how to create a Webhook Receiver and how to call the GraphQL API. The class structure of the sample application is documented by the generated [Javadoc](https://ibm-ecm.github.io/ibm-content-platform-engine-samples/ContentEventWebhookReceiver/). Some of the example logic in this sample is not necessarily realistic and might not be used in an actual Webhook Receiver application. In developing a real life Webhook Receiver application, you can remove logic that is not required. See [**Modifying the Webhook Receiver sample application**](#modifying-the-webhook-receiver-sample-application) for more details.

The sample application assumes the object store that is configured to use the webhook has a custom document class with the following structure:
- *Claim*
  - **Symbolic name:** *WebhookClaim*
  - Subclassed from Document
  - **Property Definitions**:
    - *Dollar Amount*
      - **Symbolic name:** *WebhookDollarAmount*
      - **Data type:** Float
      - **Cardinality:** Single
    - *Risk Factor*
      - **Symbolic name:** *WebhookRiskFactor*
      - **Data type:** Integer
      - **Cardinality:** Single
    - *Priority*
      - **Symbolic name:** *WebhookPriority*
      - **Data type:** String
      - **Cardinality:** Single
      - **Maximum string length:** 64
      - **Assign choice list:** *WebhookPriorityChoiceList*
        - **Choice Items:** *Critical*, *High*, *Medium*, and *Low*

The Claim document class can be imported using the [WebhookClaim.zip](files/WebhookClaim.zip) deployment package, as specified in [**Preparing the Content Platform Engine object store**](#preparing-the-content-platform-engine-object-store), or you can manually create the class and property templates.

The sample application has the following structure:
- [com.ibm.ecm.sample.webhook](https://ibm-ecm.github.io/ibm-content-platform-engine-samples/ContentEventWebhookReceiver/com/ibm/ecm/sample/webhook/package-frame.html)
  - [WebhookReceiver](https://ibm-ecm.github.io/ibm-content-platform-engine-samples/ContentEventWebhookReceiver/com/ibm/ecm/sample/webhook/WebhookReceiver.html)
    - This is the main servlet, which handles the logic for the Content Event Webhook Receiver. Whenever the Webhook External Event Action makes a call to the Webhook Receiver on the `/receiver` path of this application, such as when an event is received from the Content Platform Engine server, the `listener` method of this class will process the call. Every time an event is received, the following events occur:
    1. Parse the JSON payload from the Webhook External Event Action call
    2. Ping the Content Services GraphQL Server
    3. If the event is a CreationEvent:
       - Retrieve the Webhook Event Action and subscription created when the Receiver application started.
       - Check if the subscription that triggered the callout is associated with the first event action created by the Receiver application.
       - If the subscription that triggered the callout is the same as the first subscription created on startup, update the event action and subscription name and description. Also, change the subscription to be subscribed to UpdateEvent instead of CreationEvent. 
    4. Retrieve the source document and its properties. Note: Source object properties are in the JSON payload of the External Event Action call. The GraphQL API call to retrieve the document is only an example. In a realistic use case it might be better to parse the JSON payload for the properties instead of calling the GraphQL API unless you need to retrieve the content of the document.
    5. If this event was triggered by a CreationEvent, keep track of the object for later deletion when the Webhook Receiver sample application shuts down.
    6. Parse the JSON of the retrieved source object for specific custom properties (*WebhookDollarAmount*, *WebhookPriority*, and *WebhookRiskFactor*). These properties are defined on the class definition of the subscribed custom class *WebhookClaim*.
    7. Perform custom backend processing of the document and its custom properties. This section is left blank on purpose. In a real application, the enterprise specific processing occurs here. As this is only a sample application, it is left as an exercise for the user to provide the logic for processing the source object.
    8. If the *WebhookRiskFactor* value has not been set, update the source object to set the property to and arbitrary value (*15*). Make sure not to update the object if *WebhookRiskFactor* value has already been set, or an infinite loop will result, as each update will trigger another event.
  - [WebhookReceiverApplication](https://ibm-ecm.github.io/ibm-content-platform-engine-samples/ContentEventWebhookReceiver/com/ibm/ecm/sample/webhook/WebhookReceiverApplication.html)
    - Simple extension of the `javax.ws.rs.core.Application` class for the Content Event Webhook Receiver sample application. This extension adds important top-level classes for the REST servlet and interceptors for the application class loader.
  - [WebhookReceiverServletContextListener](https://ibm-ecm.github.io/ibm-content-platform-engine-samples/ContentEventWebhookReceiver/com/ibm/ecm/sample/webhook/WebhookReceiverServletContextListener.html)
    - Handles logic for startup and shutdown of the Content Event Webhook Receiver sample application. The startup (`contextInitialized`) handles setup of the Webhook External Event Action and it subscriptions, while the shutdown (`contextDestroyed`) handles the teardown and cleanup of the event action and subscription that was created, as well as any documents that are created as a part of driving the example.
    - When the application starts up, the following events occur:
      1. Ping the Content Services GraphQL Server.
      2. Create the Webhook External Event Action and subscription. Initially, this event action and subscription is subscribed to the CreationEvent on the *WebhookClaim* class definition. Later, the event action and subscription is modified.
      3. Parse the response from the create call to get the external event action ID for later cleanup.
      4. Retrieve the Webhook External event Action and subscription to get the subscription ID. (Note: The previous create call does not return information about the created subscription, which is why it must be fetched again. An alternative to this additional call is to specify an ID for the subscription when creating it.)
      5. Parse the response from the query to get the subscription ID for later cleanup.
    - When the application shuts down, the following events occur:
      1. Delete the Webhook External Event Action created on startup and all associated subscriptions. To do this with the GraphQL API requires an update mutation on the Webhook External Event Action to delete all associated subscriptions first and then the deletion of the event action. Both mutations are processed in one call.
      2. Delete all instances of the *WebhookClaim* that were processed by the Webhook Receiver sample application.
- [com.ibm.ecm.sample.webhook.exception](https://ibm-ecm.github.io/ibm-content-platform-engine-samples/ContentEventWebhookReceiver/com/ibm/ecm/sample/webhook/exception/package-frame.html)
  - [WebhookReceiverExceptionMapper](https://ibm-ecm.github.io/ibm-content-platform-engine-samples/ContentEventWebhookReceiver/com/ibm/ecm/sample/webhook/exception/WebhookReceiverExceptionMapper.html)
    - In the event that the Content Event Webhook External Event action callout to the receiver sample application does not have the expected HMAC credential, `HMACAuthenticationFilter` throws a `HMACSecurityException`. This class handles mapping that exception to a `UNAUTHORIZED` response code. Note that handling for other uncaught exceptions can be added to this class, or the servlet can handle the exception and return a response. It is up to the implementor to decide which approach to take with every possible exception.
  - [HMACSecurityException](https://ibm-ecm.github.io/ibm-content-platform-engine-samples/ContentEventWebhookReceiver/com/ibm/ecm/sample/webhook/exception/HMACSecurityException.html)
    - This class is a basic Runtime Exception class that is used by `HMACAuthenticationFilter` when there is a problem with the HMAC credential verification for the Content Event Webhook Receiver.
- [com.ibm.ecm.sample.webhook.util](https://ibm-ecm.github.io/ibm-content-platform-engine-samples/ContentEventWebhookReceiver/com/ibm/ecm/sample/webhook/util/package-frame.html)
  - [Constants](https://ibm-ecm.github.io/ibm-content-platform-engine-samples/ContentEventWebhookReceiver/com/ibm/ecm/sample/webhook/util/Constants.html)
    - General constants for the Content Event Webhook Receiver sample application, including constants to use for the Content Event Webhook External Event Actions and Subscriptions created by this sample application. Also includes constants to use for the key names for `ServletContext` attributes for sharing data across the sample application and the package name to use for logging.
  - [CSServerInfo](https://ibm-ecm.github.io/ibm-content-platform-engine-samples/ContentEventWebhookReceiver/com/ibm/ecm/sample/webhook/util/CSServerInfo.html)
    - This class is used for handling the Content Services server information, including the GraphQL server URL and login credentials for the user that is used to configure the Content Event Webhook and handle callback requests to process the document that triggered the Webhook's subscription. Make sure to change the information set in [CSServerInfo.properties](src/main/resources/com/ibm/ecm/sample/webhook/util/CSServerInfo.properties) to have the appropriate Content Services GraphQL server URL and Content Platform Engine admin user to use for setting up the Content Event Webhook event action and subscription and callback logic.
  - [GraphQLAPIUtil](https://ibm-ecm.github.io/ibm-content-platform-engine-samples/ContentEventWebhookReceiver/ContentEventWebhookReceiver/com/ibm/ecm/sample/webhook/util/GraphQLAPIUtil.html)
	- Utility class for handling calls to the Content Services GraphQL API.
  - [GraphQLCallTemplate](https://ibm-ecm.github.io/ibm-content-platform-engine-samples/ContentEventWebhookReceiver/ContentEventWebhookReceiver/com/ibm/ecm/sample/webhook/util/GraphQLCallTemplate.html)
	- This class is used for keeping track of templates for various GraphQL calls. See [GraphQLCallTemplate.properties](src/main/resources/com/ibm/ecm/sample/webhook/util/GraphQLCallTemplate.properties) for the GraphQL call templates.
  - [HMACAuthenticationFilter](https://ibm-ecm.github.io/ibm-content-platform-engine-samples/ContentEventWebhookReceiver/com/ibm/ecm/sample/webhook/util/HMACAuthenticationFilter.html)
    - The HMACAuthenticationFilter class implements the `ReaderInterceptor` class, which combined with the `@Provider` annotation allows this class to automatically intercept any requests before they are accepted by the REST servlet.
      This class handles the validation of the HMAC credentials that are passed by the Content Event Webhook External Event Action. On the Content Platform Engine side, the External Event Action has an External Receiver Credentials (*EevEventReceiverCredentials*) property, where the user specifies the credential type. In Content Platform Engine 5.5.4, only HMAC credentials and the `HmacSHA1` algorithm are supported. The user must specify a secret value in the External Receiver Credentials that matches the secret value on the External Event Receiver application. This secret value is then used as a cryptographic key along with the External Event action payload to generate an HMAC value.
      The HMC credential serves two purposes:
      1. Verify that the External Event Action callout is meant specifically for this Receiver application and not a different Receiver application
      2. Validate that the request has not been tampered with and is coming from the trusted sender (the Content Platform Engine server) 
  - [WebhookReceiverLogger](https://ibm-ecm.github.io/ibm-content-platform-engine-samples/ContentEventWebhookReceiver/com/ibm/ecm/sample/webhook/util/WebhookReceiverLogger.html)
    - Collection of utility methods for handling logging with the Apache logger.

---
### Modifying the Webhook Receiver sample application

When using the Webhook Receiver sample application for the first time, make sure to change the information set in [CSServerInfo.properties](src/main/resources/com/ibm/ecm/sample/webhook/util/CSServerInfo.properties) to have the appropriate Content Services GraphQL server URL and Content Platform Engine admin user to use for setting up the Content Event Webhook event action and subscription and callback logic. This file must be customized for the application's target environment in order for the sample aplication to work.

You can modify the sample application as needed to implement any required logic. A number of GraphQL calls are included as an example. The logic can be freely modified as necessary to accommodate the specific use case for the webhook. Here are some things of note when customizing the sample application:

- [build.gradle](build.gradle)
  - If additional dependencies are required, add them here. Dependencies are downloaded from [JCenter](https://bintray.com/bintray/jcenter) in the sample application, but the repository can be changed as needed.
  - To enable HTML character and newline character filtering, the `'commons-lang:commons-lang:2.6'` dependency must be uncommented. See the `WebhookReceiverLogger` class below for more information.
- [content-event-webhook-receiver.xml](files/content-event-webhook-receiver.xml)
  - The sample application deployment descriptor information is contained in this file. This file might need to be modified to accommodate the details of the Liberty server.
  - If a different context root than `/webhook` is used, change the context root here and in [CSServerInfo.properties](src/main/resources/com/ibm/ecm/sample/webhook/util/CSServerInfo.properties).
  - By default, all tracing is enabled. The `trace` level has logging related to the HMAC value validation and method enter/exit tracing. The `debug` level has logging related to the application logic (GraphQL calls, startup, shutdown, and handling incoming events). The tracing can be reduced to the `info` lever, or additional tracing can be added if needed.
  - Application name and the WAR file path can be changed in this file as well. By default, the WAR is assumed to be in the Liberty apps directory.
- [WebhookReceiver.java](src/main/java/com/ibm/ecm/sample/webhook/WebhookReceiver.java)
  - Most of the logic for handling the incoming events is in this class, so most customization must be implemented here.
    - The logic implemented for the sample application is intended more as a demonstration for how to do certain actions, rather than a realistic template. Some of the steps, like changing the event action and subscription on the creation event, can be removed if not required.
	- The sample application currently has no back-end processing. The *WebhookClaim* document properties are retrieved, but are not actually processed. If the *WebhookRiskFactor* property is null, we set it to *15*. A real application must have actual back-end business logic to handle the document.
	- If GraphQL calls are being modified or added, the code here must be modified to match up with the new or changed GraphQL calls.
	- Errors can either be handled by throwing an unhandled runtime exception, with mapping of the exception handled in [WebhookReceiverExceptionMapper.java](src/main/java/com/ibm/ecm/sample/webhook/exception/WebhookReceiverExceptionMapper.java), or the exception can be handled and an error code can be returned. If a response status other than `HTTP OK` (200) is returned, then the Content Platform Engine server retries as configured by the **Domain > Asynchronous Processing Subsystem > Retry count** parameter in the Administration Console for Content Platform Engine.
- [WebhookReceiverServletContextListener.java](src/main/java/com/ibm/ecm/sample/webhook/WebhookReceiverServletContextListener.java)
  - The logic for startup and shutdown is all contained in this class. The goal for the sample application was to configure the environment for a demonstration, then clean up the environment when done. When customizing the sample application, this is another likely class to change.
  - In a realistic use case, use a fixed ID for the event action and subscription, rather than a different one on every start up. Also, if configuration is still done on start up in a custom application, more logic must be added to handle the case where clean up did not occur.
  - Also, in a realistic use case, have an end point that could be triggered (or some other mechanism) to handle clean up of the event action, subscription, and processed documents. Deleting all of those elements on shutdown is unlikely to be realistic.
- [CSServerInfo.java](src/main/java/com/ibm/ecm/sample/webhook/util/CSServerInfo.java) and [CSServerInfo.properties](src/main/resources/com/ibm/ecm/sample/webhook/util/CSServerInfo.properties)
  - The Content Platform Engine and GraphQL environment information is kept in a properties file for easy modification without requiring recompilation. The java class loads the properties file and stores the properties as class constants for easy access by the sample application.
  - Modify all properties in CSServerInfo.properties to suit the environment where the sample application will run.
  - User credentials are stored in clear text in CSServerInfo.properties for simplicity of setup of the sample application. In a production environment, use a different approach to store, encrypt, and retrieve the user credentials.
  - Add properties as needed for environment information, such as the URL for a back-end service for handling business logic.
- [GraphQLCallTemplate.java](src/main/java/com/ibm/ecm/sample/webhook/util/GraphQLCallTemplate.java) and [GraphQLCallTemplate.properties](src/main/resources/com/ibm/ecm/sample/webhook/util/GraphQLCallTemplate.properties)
  - The templates used for building a GraphQL API call are kept in the properties file for easy modification without requiring recompilation. The java class loads the properties file and stores the properties as class constants for easy access by the sample application.
  - When customizing the sample application, you are likely to change this class. The GraphQL call templates can be modified as needed, or additional templates can be added for new queries or mutations. When making changes, make sure that the execution logic for replacing the variables matches the call template in the properties file, for example, the order and number of variables that are replaced must match what is in the properties file.
- [GraphQLAPIUtil.java](src/main/java/com/ibm/ecm/sample/webhook/util/GraphQLAPIUtil.java)
  - The [Apache HttpClient](https://hc.apache.org/httpcomponents-client-4.5.x/index.html) library is used for handling connections to the GraphQL API server. This library can be swapped out for a different library, if desired.
  - The sample code has configured the HttpClient library to use the protocol `TLSv1.2` to connect to the GraphQL API server. If a different protocol is needed, the protocol in the sample code can be changed.
  - Basic authentication is used when connecting to the GraphQL API. Also, the user credentials are saved in clear-text in [CSServerInfo.properties](src/main/resources/com/ibm/ecm/sample/webhook/util/CSServerInfo.properties) and passed as a Base64 encodeded string on the `Authorization` header. A more secure (preferably encrypted) mechanism for handling the credentials is left as an exercise for the developer making a custom Webhook Receiver application. Other authentication mechanisms are also a possibilty, such as using OAuth2.0 or OpenID Connect (OIDC), support for which was recently added for Content Platform Engine and GraphQL in the 5.5.4 release. For more information, see the topic [Configuring advanced authentication](https://www.ibm.com/support/knowledgecenter/SSNW2F_5.5.0/com.ibm.p8.containers.doc/containers_gqladvauth.htm) for more information.
- [HMACAuthenticationFilter.java](src/main/java/com/ibm/ecm/sample/webhook/util/HMACAuthenticationFilter.java)
  - In Content Platform Engine 5.5.4, only HMAC credentials and the `HmacSHA1` algorithm are supported. Future releases may potentially add support for additional credential types and alogithms. This class can be modified in the event a different supported credential and/or algorithm is used.
- [WebhookReceiverLogger](src/main/java/com/ibm/ecm/sample/webhook/util/WebhookReceiverLogger.java)
  - The same class is used for all tracing in the application. It might be desirable to change this class or have every class use a different logger.
  - In a realistic application, filter out newline and HTML characters, as user-provided strings can potentially contain fake log messages [CWE-117: Improper Output Neutralization for Logs](https://cwe.mitre.org/data/definitions/117.html). The sample application has the code commented out, as the response JSON from the GraphQL API logged in the debug trace is easier to read with newline characters. If this application is used as the bases for a real application, edit the [build.gradle](build.gradle) file to add the `commons-lang` library, import `org.apache.commons.lang.StringEscapeUtils`, and uncomment the relevant code in this class.


---
### Building the Webhook Receiver sample application
This project uses the [Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html) to download a Gradle distribution to execute its build. The Gradle distribution and build dependencies are downloaded from [JCenter](https://bintray.com/bintray/jcenter). Execute the build by running one of the following scripts located in the root of this folder. The Gradle distribution will be downloaded if it does not already exist locally.

- **Windows**: `gradlew.bat war`
- **Linux/Mac**: `./gradlew war`

Before building the sample application, change the information set in [CSServerInfo.properties](src/main/resources/com/ibm/ecm/sample/webhook/util/CSServerInfo.properties) to have the appropriate Content Services GraphQL server URL and Content Platform Engine admin user to use for setting up the Content Event Webhook event action and subscription and callback logic. For the sample application to work, you must customize the file for the environment that the application will run in. See [**Modifying the Webhook Receiver sample application**](#modifying-the-webhook-receiver-sample-application) for more information.


---
### Deploying the Webhook Receiver sample application
The sample application has been tested only on a WebSphere Liberty server, as the Content Services GraphQL API only supports WebSphere Liberty. 

To deploy the sample application:
  1. Follow the steps in [**Preparing the Content Platform Engine object store**](#preparing-the-content-platform-engine-object-store).
  2. Edit [CSServerInfo.properties](src/main/resources/com/ibm/ecm/sample/webhook/util/CSServerInfo.properties) to have the appropriate Content Services GraphQL server URL and Content Platform Engine admin user to use for setting up the Content Event Webhook event action and subscription and callback logic. See the topic [**Modifying the Webhook Receiver sample application**](#modifying-the-webhook-receiver-sample-application) for more information.
  3. If needed, edit [content-event-webhook-receiver.xml](files/content-event-webhook-receiver.xml). See topic [**Modifying the Webhook Receiver sample application**](#modifying-the-webhook-receiver-sample-application) for more information.
  4. Build the sample application.  See topic [**Building the Webhook Receiver sample application**](#building-the-webhook-receiver-sample-application) for more information.
  5. Copy the built WAR file from `build/libs/content-event-webhook-receiver.war` to the Liberty apps directory.
  6. Copy the modified [content-event-webhook-receiver.xml](files/content-event-webhook-receiver.xml) file to the Liberty `configDropins/defaults` directory (or other appropriate directory).
  7. Start the Liberty server.

---
### Using the Webhook Receiver sample application
When the sample application is started, it will automatically configure the webhook for the specified Content Platform Engine object store. Once the startup application logic has finished, you can trigger the webhook by doing the following:
  1. Log into an IBM Content Navigator desktop with a browse feature that has a repository that matches the Content Platform Engine object store for which the webhook is configured.
  2. Create an instance of the *Claim* (symbolic name *WebhookClaim*) in the object store.
    - Set the *Dollar Amount* and *Risk Factor*, but leave the *Priority* property blank.
  3. After waiting a small amount of time, open or refresh the created document. The *Priority* property should have a value of *15*.

If you look at the Liberty logs, you see `info` log entries from the `com.ibm.ecm.sample.webhook` package. If a problem occurs, you see `error` log entries as well. The Liberty trace logs also have `trace` and `debug` log entries if you specified the appropriate logging level for the `com.ibm.ecm.sample.webhook` package.

When you shut down the sample application, it deletes the Webhook External event action and subscription, as well as any documents of the *WebhookClaim* class that you created that were processed. Note that sufficient time must be given to the application for this to work. If the sample application is running in a [Docker container](https://www.docker.com/resources/what-container), shutting down the container might not give sufficient time for the sample application to fully run its shutdown procedure.

