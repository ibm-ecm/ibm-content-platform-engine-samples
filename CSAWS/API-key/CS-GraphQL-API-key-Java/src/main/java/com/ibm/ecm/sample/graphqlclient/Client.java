/*
 * Licensed Materials - Property of IBM (c) Copyright IBM Corp. 2023 All Rights Reserved.
 * 
 * US Government Users Restricted Rights - Use, duplication or disclosure restricted by GSA ADP Schedule Contract with
 * IBM Corp.
 * 
 * DISCLAIMER OF WARRANTIES :
 * 
 * Permission is granted to copy and modify this Sample code, and to distribute modified versions provided that both the
 * copyright notice, and this permission notice and warranty disclaimer appear in all copies and modified versions.
 * 
 * THIS SAMPLE CODE IS LICENSED TO YOU AS-IS. IBM AND ITS SUPPLIERS AND LICENSORS DISCLAIM ALL WARRANTIES, EITHER
 * EXPRESS OR IMPLIED, IN SUCH SAMPLE CODE, INCLUDING THE WARRANTY OF NON-INFRINGEMENT AND THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE. IN NO EVENT WILL IBM OR ITS LICENSORS OR SUPPLIERS BE LIABLE FOR
 * ANY DAMAGES ARISING OUT OF THE USE OF OR INABILITY TO USE THE SAMPLE CODE, DISTRIBUTION OF THE SAMPLE CODE, OR
 * COMBINATION OF THE SAMPLE CODE WITH ANY OTHER CODE. IN NO EVENT SHALL IBM OR ITS LICENSORS AND SUPPLIERS BE LIABLE
 * FOR ANY LOST REVENUE, LOST PROFITS OR DATA, OR FOR DIRECT, INDIRECT, SPECIAL, CONSEQUENTIAL, INCIDENTAL OR PUNITIVE
 * DAMAGES, HOWEVER CAUSED AND REGARDLESS OF THE THEORY OF LIABILITY, EVEN IF IBM OR ITS LICENSORS OR SUPPLIERS HAVE
 * BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
 */
package com.ibm.ecm.sample.graphqlclient;

import org.json.JSONArray;
import org.json.JSONObject;

public class Client {
    private static String className = "Client";

    public static void main(String[] args) {
        GraphQLAPIUtil.getSubDomainToken();
        pingServer();
        simpleQuery();
    }
    
    private static void pingServer() {
        String methodName = "pingServer";
        try {
            // Ping GraphQL server first before continuing
            String serverURL = CSServerInfo.CS_SERVER_GRAPHQL_URL;
            int index = serverURL.indexOf("/graphql");
            String pingURL = serverURL.substring(0, index);
            pingURL = pingURL +"/ping";
            
            JSONObject jsonGraphQLResponse =
                    GraphQLAPIUtil.callGraphQLAPI(pingURL, null);

            // Handle errors in JSON, if any
            if (jsonGraphQLResponse.has("errors")) {
                JSONArray jsonResponseErrors = jsonGraphQLResponse
                        .getJSONArray("errors");

                // If there is an error, return error based on the first one
                if (jsonResponseErrors.length() > 0) {
                    Object graphQLErrorObj = jsonResponseErrors.get(0);
                    JSONObject graphQLError = new JSONObject(
                            graphQLErrorObj.toString());

                    String errorMessage = graphQLError.getString("message");

                    // Return with the exception
                    ClientLogger.error("Error ping graphql",
                            errorMessage);
                    ClientLogger.exiting(className,
                            methodName);
                    System.out.println(errorMessage);
                }
            }
            else
            {
                System.out.println(jsonGraphQLResponse);
            }
            
        } catch (Exception e) {
            ClientLogger.error("Error ping graphql", e);
            System.out.println(e);
        }
    }
    
    private static void simpleQuery()
    {
        String methodName = "simpleQuery";
        try {
            // Assume the token is still valid. Users should have their own logic to handle token expiration. 
            String objectStoreId = CSServerInfo.CS_SERVER_OBJECTSTORE;
            
            ClientLogger.debug("  =====+++++=====!!!!! "
                    + "callGraphQLAPI ping with objectStoreId="
                    + objectStoreId);
            String graphQLSchema = String.format(
                    GraphQLCallTemplate.QUERY_ROOT_FOLDER,
                    objectStoreId);
            
            String serverURL = CSServerInfo.CS_SERVER_GRAPHQL_URL;
            
            JSONObject jsonGraphQLResponse =
                    GraphQLAPIUtil.callGraphQLAPI(serverURL, graphQLSchema);

            // Handle errors in JSON, if any
            if (jsonGraphQLResponse.has("errors")) {
                JSONArray jsonResponseErrors = jsonGraphQLResponse
                        .getJSONArray("errors");

                // If there is an error, return error based on the first one
                if (jsonResponseErrors.length() > 0) {
                    Object graphQLErrorObj = jsonResponseErrors.get(0);
                    JSONObject graphQLError = new JSONObject(
                            graphQLErrorObj.toString());

                    String errorMessage = graphQLError.getString("message");

                    // Return with the exception
                    ClientLogger.error("Error query graphql",
                            errorMessage);
                    ClientLogger.exiting(className,
                            methodName);
                    System.out.println(errorMessage);
                }
            }
            else
            {
                System.out.println(jsonGraphQLResponse);
            }
            
        } catch (Exception e) {
            ClientLogger.error("Error query graphql", e);
            System.out.println(e);
        }
    }
}
