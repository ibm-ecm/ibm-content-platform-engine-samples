# GraphQL client using API key Java sample application
# Content Engine Java API sample application for API keys in a Content Services on AWS environment
Java snippet showing how to exchange an API key and secret for OIDC JWT, and then pass that JWT into the OpenTokenCredentials class of the CE API. 
---
# Setting up the development environment

#### Prerequisites

#### 1. Check out this repo to your local disk, then go into the project folder.

#### 2. Modify cejavaapikey.properties to reflect the CSAWS instance you are connecting to. 

#### 3. Obtain a copy of the CE jace.jar and place it in the libs sub-directory (or elsewhere in your classpath)  Note: you can download the CE Java API files from the Downloads tab on the CSAWS landing page)

#### 4. Obtain a copy of json.jar from JCenter or other repository and place that in your classpath as well

#### 5. Build the application.  The build.gradle file in this distribution can be used to build in a gradle environment 

#### 6. Run the application.  The runit.bsh script can be used to run the sample for Unix environments

## Project files
- [cejavaapikey.java]
  - The getOAuthAccessToken shows how your client app can pass your service user Id and secret to the APIC service to authenticate and obtain an OIDC JWT that will grant access to the CSAWS API's
  - The code then shows how to pass this JWT into the OpenTokenCredentials class to initialize the CE Java API
  - Subsequent code uses the Java PrivilegedExceptionAction interface to execute CE Java API code in the authentication context contained within the OpenTokencredentials instance
- [CEproperties.java]
  - This class uses the Java Properties class to read configuration properties from cejavaapikey.properties
- [cejavaapikey.properties]
  - APIC properties: enter your service user Id in APIC_ClientId and your API key value in APIC_ClientSecret
  - Enter the Content Engine Web Service (CEWS) endpoint for your CSAWS tenant here.  This will have a value like: https://<Your sub-domain>.content.automation.ibm.com/wsi/FNCEWS40MTOM  where <Your sub-domain> is replaced with the sub-domain that you use when logging into the CSAWS landing page
  - The APIC

## Notes
  - Service user/key credentials are stored in clear text in cejavaapikey.properties for simplicity of setup of the sample application. In a production environment, use a different approach to store, encrypt, and retrieve the user credentials.
  - Add properties as needed for environment information, such as the URL for a back-end service for handling business logic.
  - The JWT token that you obtain from APIC is valid only for two hours.  If your application will be long running, then you should have logic to obtain a new token and pass it into OpenTokenConnections before the token expiration occurs, to prevent errors.
  
