# Usage
This program demonstrates simple implementations of a GraphQL program by leveraging AWS GraphQL's API.

# Prerequisite
- Functional Python3 instance, downloadable from: https://www.python.org/downloads/
- Python Requests library:
`pip install requests`

# Instruction
Before using this program, make sure to edit config.py to match with the intended endpoints.

Template of Variables:
- GQL_URL = `${InstanceName}.content.automation.ibm.com/content-services-graphql/graphql`
- APIC_TOKEN_URL =  `https://api-9o4.us-east-a.apiconnect.ibmappdomain.cloud/ibmcontentservices/csprod/${InstanceName}/token`
- SERVICE_USER_ID = `USERNAME@INSTANCENAME.fid`
- FILE_PATH = '/a/b/c'

Sample:
- GQL_URL = 'gqlsample.content.automation.ibm.com/content-services-graphql/graphql'
- APIC_TOKEN_URL =  'https://api-9o4.us-east-a.apiconnect.ibmappdomain.cloud/ibmcontentservices/csprod/gqlsample/token'
- SERVICE_USER_ID = 'TestUser@gqlsample.fid'
- SERVICE_USER_API_KEY = 'AA1bc2d%y*' 
- FILE_PATH = '/Users/test/Data'

To launch the program, call generator.py as a python program then follow the prompts.

`Python3 sample.py`

# Notes
For api generation usage, large numbers can cause a exponentially large amount of requests to be made to the graphql endpoint.


