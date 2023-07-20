# GraphQL client using API key Java sample application
Java snippet for exchanging API key for API key JWT of service user and calling CS graphQL API using the JWT
---
# Setting up the development environment

#### Prerequisites

#### 1. Check out this repo to your local disk, then go into the project folder.

#### 2. Modify CSServerInfo.properties to reflect the CSAWS instance you are connecting to. 

#### 3. Build the application and run it. 

## Project 
- [Client.java]
  - First call API Connect with service id and key to get JWT token
  - Do a ping to GraphQL server with the JWT token to get the ECM-CS-XSRF-Token
  - Call GraphQL API with JWT token and ECM-CS-XSRF-Token in header
- [CSServerInfo.java] and [CSServerInfo.properties]
  - The API Connector and GraphQL environment information is kept in a properties file for easy modification without requiring recompilation. The java class loads the properties file and stores the properties as class constants for easy access by the sample application.
  - Modify all properties in CSServerInfo.properties to suit the environment where the sample application will run.
  - Service user/key credentials are stored in clear text in CSServerInfo.properties for simplicity of setup of the sample application. In a production environment, use a different approach to store, encrypt, and retrieve the user credentials.
  - Add properties as needed for environment information, such as the URL for a back-end service for handling business logic.
- [GraphQLCallTemplate.java] and [GraphQLCallTemplate.properties]
  - The templates used for building a GraphQL API call are kept in the properties file for easy modification without requiring recompilation. The java class loads the properties file and stores the properties as class constants for easy access by the sample application.
  - When customizing the sample application, you are likely to change this class. The GraphQL call templates can be modified as needed, or additional templates can be added for new queries or mutations. When making changes, make sure that the execution logic for replacing the variables matches the call template in the properties file, for example, the order and number of variables that are replaced must match what is in the properties file.
- [GraphQLAPIUtil.java]
  - The [Apache HttpClient](https://hc.apache.org/httpcomponents-client-4.5.x/index.html) library is used for handling connections to the GraphQL API server. This library can be swapped out for a different library, if desired.
  - The sample code has configured the HttpClient library to use the protocol `TLSv1.2` to connect to the GraphQL API server. If a different protocol is needed, the protocol in the sample code can be changed.
  - JWT token is used to connect to call GraphQL API. 
  
