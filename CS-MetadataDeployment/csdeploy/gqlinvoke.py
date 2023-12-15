#  Licensed Materials - Property of IBM (c) Copyright IBM Corp. 2023 All Rights Reserved.
 
#  US Government Users Restricted Rights - Use, duplication or disclosure restricted by GSA ADP Schedule Contract with
#  IBM Corp.
 
#  DISCLAIMER OF WARRANTIES :
 
#  Permission is granted to copy and modify this Sample code, and to distribute modified versions provided that both the
#  copyright notice, and this permission notice and warranty disclaimer appear in all copies and modified versions.
 
#  THIS SAMPLE CODE IS LICENSED TO YOU AS-IS. IBM AND ITS SUPPLIERS AND LICENSORS DISCLAIM ALL WARRANTIES, EITHER
#  EXPRESS OR IMPLIED, IN SUCH SAMPLE CODE, INCLUDING THE WARRANTY OF NON-INFRINGEMENT AND THE IMPLIED WARRANTIES OF
#  MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE. IN NO EVENT WILL IBM OR ITS LICENSORS OR SUPPLIERS BE LIABLE FOR
#  ANY DAMAGES ARISING OUT OF THE USE OF OR INABILITY TO USE THE SAMPLE CODE, DISTRIBUTION OF THE SAMPLE CODE, OR
#  COMBINATION OF THE SAMPLE CODE WITH ANY OTHER CODE. IN NO EVENT SHALL IBM OR ITS LICENSORS AND SUPPLIERS BE LIABLE
#  FOR ANY LOST REVENUE, LOST PROFITS OR DATA, OR FOR DIRECT, INDIRECT, SPECIAL, CONSEQUENTIAL, INCIDENTAL OR PUNITIVE
#  DAMAGES, HOWEVER CAUSED AND REGARDLESS OF THE THEORY OF LIABILITY, EVEN IF IBM OR ITS LICENSORS OR SUPPLIERS HAVE
#  BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

""" Module containing classes to maintain connection to CPE GraphQL Endpoint"""
import json
import uuid
import requests

class GraphqlConnection:
    """ Class containing information for graphql request's authentication"""
    def __init__(self, url:str, token_url: str = None, token: str = None, ssl_enabled:bool = True) -> None:
        self.url = url
        self.token_url = token_url
        self.headers = {}
        self.payload = {}
        self.xsrf_token = None
        self.token = token
        self.auth_user = None
        self.auth_pass = None
        self.ssl_enabled = ssl_enabled


    def initialize_apic(self, user_id:str, api_key:str) -> None:
        """initialize class with apic auth information
        Args:
            userId (str): user id fetched from API Key Gen
            apiKey (str): api key fetched from API Key Gen
        """
        self.headers = {
            'X-IBM-Client-Id': user_id,
            'X-IBM-Client-Secret': api_key,
        }

    def initialize_oauth(self, grant_type:str, scope:str,
                        username:str = None, password:str = None,
                        client_id:str = None, client_secret:str = None
                        ) -> None:
        """initialize connection with oauth information
        Args:

            username (str): username 
            password (str): password
            grant_type (str): oauth's grant type
            scope (str): oauth's scope
            client_id (str): oauth client id
            client_secret (str): oauth client secret
        """
        self.payload = {
            'grant_type': grant_type,
            'scope': scope,
        }
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        if (username and password) and (username != 'REPLACE' and password != 'REPLACE'):
            self.payload['username'] = username
            self.payload['password'] = password

        if (client_id and client_secret) and (client_id != 'REPLACE' and client_secret != 'REPLACE'):
            self.auth_user = client_id
            self.auth_pass = client_secret


    def initialize_basic(self, username:str, password:str) -> None:
        """inititialize class with basic auth information
        Args:
            username (str): username
            password (str): password
        """
        self.xsrf_token = str(uuid.uuid4())
        self.auth_user = username
        self.auth_pass = password

    def get_token(self) -> None:
        """Execute request to get token for non-basic auth
        """
        self.xsrf_token = str(uuid.uuid4())
        operation = "POST" if self.payload else "GET"
        auth = (self.auth_user, self.auth_pass) if (self.auth_user and self.auth_pass) else None
        response = requests.request(operation, self.token_url,
                                    headers=self.headers, data=self.payload,
                                    timeout=300, verify=self.ssl_enabled,
                                    auth = auth)
        try:
            if "token" in response.json():
                self.token = response.json()["token"]
            elif "access_token" in response.json():
                self.token = response.json()["access_token"]
            else:
                raise Exception("Invalid JSON in Response")
        except:
            print(f"Request failed with status code {response.status_code}")
            try:
                error_data = response.json()
                print("Response JSON:")
                print(error_data)
            except ValueError:
                print("Response Text:")
                print(response.text)

    def exchange_iam_token(self, exchange_token_url: str) -> None:
        """Execute request to get Zen Token from IAM Token
        """
        self.get_token()
        headers = {'username': self.payload['username'], 'iam-token': self.token}
        response = requests.request("GET", exchange_token_url,
                                    headers=headers,
                                    timeout=300, verify=self.ssl_enabled)
        try:
            self.token = response.json()["accessToken"]
        except:
            print(f"Request failed with status code {response.status_code}")
            try:
                error_data = response.json()
                print("Response JSON:")
                print(error_data)
            except ValueError:
                print("Response Text:")
                print(response.text)

class GraphqlRequest:
    """Class used to execute graphql queries and mutations"""
    def __init__(self, gql_connection:GraphqlConnection) -> None:
        self.gql_connection = gql_connection

    def execute_request(self, query:str, variables=None):
        """Send Post request to graphql endpoint

        Args:
            query (str): query being sent
            variables (_type_, optional): variables to be sent with query. Defaults to None.
        Returns:
            _type_: _description_
        """
        headers = {
            'Content-Type': 'application/json',
            'ECM-CS-XSRF-Token': self.gql_connection.xsrf_token
        }
        cookies = {
            'ECM-CS-XSRF-Token': self.gql_connection.xsrf_token
        }

        if self.gql_connection.token:
            headers['Authorization'] = 'Bearer ' + self.gql_connection.token
            auth = None
        elif (self.gql_connection.auth_user and self.gql_connection.auth_pass):
            auth = (self.gql_connection.auth_user, self.gql_connection.auth_pass)
        else:
            print("Invalid Authentication method for gqlconnection")

        inclvars = variables if variables else {}
        jsonpload = {'query': query, 'variables':inclvars}
        # Debug >>
        # print("Executing Graphql request with payload ...")
        # print(json.dumps(jsonpload, indent=4))
        response = requests.post(url=self.gql_connection.url, headers=headers,
                                json=jsonpload, cookies=cookies, timeout = 300,
                                verify=self.gql_connection.ssl_enabled, auth=auth)
   
        if response.status_code != 200:
            print(f"Request failed with status code {response.status_code}")
            try:
                error_data = response.json()
                print("Response JSON:")
                print(error_data)
            except ValueError:
                print("Response Text:")
        return response
