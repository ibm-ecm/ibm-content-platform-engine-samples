# CS-GraphQL-javascript-samples <br/>
Javascript snippet for different document/folder operations using CS graphQL API<br/>
<br/>
Examples of foundation operations include:<br/>
- Create document<br/>
- Download document with content<br/>
- Check-out/Check-in document<br/>
- Create folder and sub-folders<br/>
- Add/file documents into folder<br/>
- Search<br/>
   - Documents<br/>
   - Folder navigation/search for folder containees <br/>
   - Documents where search criteria involves multiple joined classes<br/>
- Retrieving metadata - classDescription<br/>
- Retrieving subclasses of a certain class<br/>
- Retrieving a domain and its object stores<br/>
- Retrieving a class description & all its subclasses’ property descriptions<br/>
- Getting total count of Object Search<br/>
- Update permissions<br/>
- Multiple Repository Object Searches<br/>
- Update custom single value<br/>
- Generic mutations with dependent objects<br/>

# Setting up the development environment

#### Prerequisites

1. Data prerequisite for Search with JOIN operation i.e Documents where search criteria involves       multiple joined classes
   1. Create subclasses of Document class from "ACCE console" 
      1. LoanApplicationDocument
      2. Lender

      Refer link for the procedure : https://www.ibm.com/support/knowledgecenter/SSNW2F_5.5.0/com.ibm.p8.ce.admin.tasks.doc/classes/cl_create_a_subclass.htm

   2. Create Properties Templates from "ACCE console" 
      1. Display Name and Symbolic Name : BorrowerName, Data Type : String 
      2. Display Name and Symbolic Name : LenderName, Data Type : String 
      3. Display Name and Symbolic Name : LoanApplicationNumber, Data Type : Integer 
   
      Refer link for the procedure : https://www.ibm.com/support/knowledgecenter/SSNW2F_5.5.0/com.ibm.p8.ce.admin.tasks.doc/properties/pr_create_property_template.htm 

   3. Assign properties to the subclasses from "ACCE console"
      1. LoanApplicationDocument properties : BorrowerName, LenderName, LoanApplicationNumber 
      2. Lender properties : LenderName 
   
      Refer link for the procedure : https://www.ibm.com/support/knowledgecenter/SSNW2F_5.5.0/com.ibm.p8.ce.admin.tasks.doc/properties/pr_assign_properties_to_a_class.htm 

   4. Execute "Create Document" operation from the sample application atleast once prior to "Search with JOIN" operation
2. Allowing CORS for GraphQL server
   1. Navigate to GraphQL Host server and find server.xml in root directory
   2. Edit server.xml and add one of the following snippet in the following in <Server> Tag and edit "REPLACE_WITH_ORIGIN" with your sample script host(request origin url):
   Whitelist Origin:
   ```html
   <cors domain="/content-services-graphql"
        allowedOrigins= "REPLACE_WITH_ORIGIN"
        allowedMethods="GET, POST, OPTIONS"
        allowedHeaders="Connection,Pragma,Cache-Control,XSRFtoken,Origin,User-Agent,Content-Type,Content-Length,Accept-Control-Request-Method,Accept-Control-Request-Headers,Accept,Referer,Accept-Encoding,Accept-Language,DNT,Host,Content-Length,Cache-control,Cookie,Authorization"
        exposeHeaders="Content-Disposition,Content-Length,Content_Type,Content-Language,X-Powered-By,Date,Allow,Transfer-Encoding,$WSEP,DNT,Access-Control-Allow-Credentials,Access-Control-Allow-Headers,Access-Control-Allow-Max-Age,Access-Control-Allow-Methods,Access-Control-Allow-Origin,Access-Control-Expose-Headers,Connection,Cache-control,Cookie,x-content-download"
        allowCredentials="true"
        maxAge="3600" />
   ```
   Open Cors:
   ```html
   <cors domain="/content-services-graphql"
        allowedOrigins="*"
        allowedMethods="GET, POST, OPTIONS"
        allowedHeaders="Connection,Pragma,Cache-Control,XSRFtoken,Origin,User-Agent,Content-Type,Content-Length,Accept-Control-Request-Method,Accept-Control-Request-Headers,Accept,Referer,Accept-Encoding,Accept-Language,DNT,Host,Content-Length,Cache-control,Cookie,Authorization"
        exposeHeaders="Content-Disposition,Content-Length,Content_Type,Content-Language,X-Powered-By,Date,Allow,Transfer-Encoding,$WSEP,DNT,Access-Control-Allow-Credentials,Access-Control-Allow-Headers,Access-Control-Allow-Max-Age,Access-Control-Allow-Methods,Access-Control-Allow-Origin,Access-Control-Expose-Headers,Connection,Cache-control,Cookie,x-content-download"
        allowCredentials="true"
        maxAge="3600" />
   ```


#### 1. Check out this repo to your local disk, then go into the project folder.


#### 2. Deploy the application (samples.war):

   - Follow instructions based on your system:
      - [Liberty](https://www.ibm.com/docs/en/was-liberty/base?topic=deploying-applications-in-liberty) 
      - [WebSphere](https://www.ibm.com/docs/en/elo-p/2.0.0?topic=app-websphere-application-server)

## Project Structure

- app.js - Service code used to interact with graphQL API. User selection for operations comes to this      service layer according to which query has been selected from graphQL.js and passed as param to http (GraphQL API)call. Here XMLHttpRequest is used to make API call

- config.js - File for storing creadentials and GraphQL URL

- dataHandler.js - Contains functions for parsing GraphQL response for each operations

- graphQL.js - Contains all graphQL queries for different document operations and also process response coming from API to display on UI

- index.html - The entry of application and the main UI

- README.md - Details about what operations are supported and how to setup/run the sample application.

- samples.war - All above files zipped into ready to deploy war file.
