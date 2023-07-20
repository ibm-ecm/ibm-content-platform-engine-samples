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

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URI;
import org.apache.http.HttpHeaders;
import org.apache.http.HttpResponse;
import org.apache.http.StatusLine;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.utils.URIBuilder;
import org.apache.http.conn.ssl.SSLConnectionSocketFactory;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.ssl.SSLContexts;
import org.json.JSONObject;
import org.apache.http.Header;

/**
 * Utility class for handling calls to the Content Services GraphQL API.
 * 
 * This class will use the TLS 1.2 protocol for calls to the GraphQL API. If a
 * different protocol is required, the protocol can be changed in the code for
 * this class.
 */
public class GraphQLAPIUtil {

    private static String xsrf_token = null;
    private static String token_name = "ECM-CS-XSRF-Token";
    private static String jwt_token = null;
    protected static String getJwtToken()
    {
        return jwt_token;
    }
    /**
     * Handles calls to the Content Services GraphQL API.
     * 
     * @param graphQLCommand
     *            GraphQL command, either a query or mutation, to pass to the
     *            Content Services GraphQL API
     * @return Response for the call to the Content Services GraphQL API
     */
    public static JSONObject callGraphQLAPI(String csServerURL, String graphQLCommand) {
        String method = "callGraphQLAPI";
        ClientLogger.entering("GraphQLAPIUtil", method);

        JSONObject jsonGraphQLResponse = null;
        HttpResponse response = null;
        CloseableHttpClient httpClient = null;
        BufferedReader breader = null;

        try {
            /*
             * Create HTTPClient and have it use TLSv1.2. If you do not wish to
             * force TLSv1.2 to be used, you can change the protocol or
             * completely remove the setSSLSocketFactory() call from the
             * HttpClientBuilder call.
             */
            SSLConnectionSocketFactory sslConnectionSocketFactory =
                    new SSLConnectionSocketFactory(
                    SSLContexts.createDefault(), new String[] { "TLSv1.2" },
                    null,
                    SSLConnectionSocketFactory.getDefaultHostnameVerifier());

            httpClient = HttpClientBuilder.create()
                    .setSSLSocketFactory(sslConnectionSocketFactory).build();

            /*
             * The sample application uses jwt token authentication when connecting
             * to the GraphQL API. 
             */
            String auth_token = CSServerInfo.CS_SERVER_TOKEN;
            if (auth_token == null)
                auth_token = jwt_token;
            
            /*
             * Build the URL to the GraphQL API using the base URL from
             * CSServerInfo.properties and adding the path for GraphQL
             */
            URI uri = new URIBuilder(csServerURL).build();

            // Set headers for GraphQL API call
            HttpPost httpPost = new HttpPost(uri);
            httpPost.setHeader(HttpHeaders.AUTHORIZATION, "Bearer "+ auth_token);
            httpPost.addHeader("Accept", "application/json");
            if (xsrf_token != null)
            {
                httpPost.addHeader("Cookie", token_name+"="+xsrf_token);
                httpPost.addHeader(token_name, xsrf_token);
                
            }

            /*
             * Pass GraphQL API call via the value for a query parameter using
             * JSON.
             * 
             * Note that while GraphQL itself is similar to JSON, it is
             * different from JSON in subtle ways and thus has to be passed as a
             * String, rather than converted to a JSON object.
             */
            if (graphQLCommand != null)
            {
                JSONObject jsonGraphQLCommand = new JSONObject();
                jsonGraphQLCommand.put("query", graphQLCommand);
                StringEntity jsonQueryEntity = new StringEntity(
                        jsonGraphQLCommand.toString());
                httpPost.setEntity(jsonQueryEntity);
                httpPost.addHeader("content-type", "application/json");
            }
            else
            {
                //it's ping cmd
            }

            // Trace statement to show the arguments for the GraphQL API call
            ClientLogger.debug("calling GraphQLAPI on " + csServerURL
                    + "  with " + graphQLCommand);
            ClientLogger.debug("httpPost = " + httpPost);

            // Handle the response
            response = httpClient.execute(httpPost);
            StatusLine statusLine = response.getStatusLine();
            
            Header[] xsrf_token_headers = response.getHeaders(token_name);
            
            if (xsrf_token_headers != null) {
                for (Header h : xsrf_token_headers) {
                    if (h != null) {
                        xsrf_token = h.getValue();
                        break;
                    }
                }
            }

            // Trace statement to show the response from the GraphQL API call
            ClientLogger.debug("statusLine = "
                    + statusLine.toString());
            ClientLogger.debug("response = " + response);

            // Get response string
            breader = new BufferedReader(new InputStreamReader(
                    response.getEntity().getContent()));
            StringBuilder responseString = new StringBuilder();
            String line = "";
            while ((line = breader.readLine()) != null) {
                responseString.append(line);
            }

            /*
             * Parse response string as a JSON object and use a trace statement
             * to show the formatted response
             */
            String responseGraphQL = responseString.toString();
            jsonGraphQLResponse = new JSONObject(responseGraphQL);
            ClientLogger.debug("responseGraphQL = "
                    + jsonGraphQLResponse.toString(2) + "\n\n");

        } catch (Exception ex) {
            ClientLogger.error(
                    "Could not submit GraphQL API call.", ex);
        } finally {
            // Close the Buffered Reader
            try {
                if (breader != null) {
                    breader.close();
                }
            } catch (IOException e) {

            }
            // Close the HTTP connection
            try {
                if (httpClient != null) {
                    httpClient.close();
                }
            } catch (IOException e) {

            }
            
            ClientLogger.exiting("GraphQLAPIUtil", method);
        }

        return jsonGraphQLResponse;
    }
    
    protected static String getSubDomainToken()
    {
        String JWTToken = null;
        String method = "getSubDomainToken";
        ClientLogger.entering("GraphQLAPIUtil", method);
        
        HttpResponse response = null;
        CloseableHttpClient httpClient = null;
        BufferedReader breader = null;
        JSONObject jsonResponse = null;
        
        try
        {
            SSLConnectionSocketFactory sslConnectionSocketFactory =
                    new SSLConnectionSocketFactory(
                    SSLContexts.createDefault(), new String[] { "TLSv1.2" },
                    null,
                    SSLConnectionSocketFactory.getDefaultHostnameVerifier());
    
            httpClient = HttpClientBuilder.create()
                    .setSSLSocketFactory(sslConnectionSocketFactory).build();
    
            /*
             * The sample application uses api key to get jwt token from API Connector
             */
            /*
             * Build the URL to the API Connector endpoint
             */
            URI uri = new URIBuilder(CSServerInfo.API_ENDPOINT).build();
    
            // Set headers for API Connector call call
            HttpGet httpGet = new HttpGet(uri);
           
            httpGet.addHeader("X-IBM-Client-Id", CSServerInfo.CLIENT_ID);
            httpGet.addHeader("X-IBM-Client-Secret", CSServerInfo.CLIENT_SECRET);

            // Trace statement to show the arguments for the GraphQL API call
            ClientLogger.debug("calling APIC on " + uri
                    );
            ClientLogger.debug("httpGet = " + httpGet);

            // Handle the response
            response = httpClient.execute(httpGet);
            
            breader = new BufferedReader(new InputStreamReader(
                    response.getEntity().getContent()));
            StringBuilder responseString = new StringBuilder();
            String line = "";
            while ((line = breader.readLine()) != null) {
                responseString.append(line);
            }

            /*
             * Parse response string as a JSON object and use a trace statement
             * to show the formatted response
             */
            String responseGraphQL = responseString.toString();
            jsonResponse = new JSONObject(responseGraphQL);
            ClientLogger.debug("responseFromApic = "
                    + jsonResponse.toString(2) + "\n\n");
            jwt_token = (String)jsonResponse.get("token");
            
            
        } catch (Exception ex) {
            ClientLogger.error(
                    "Could not submit call to APIC.", ex);
        } finally {
            // Close the Buffered Reader
            try {
                if (breader != null) {
                    breader.close();
                }
            } catch (IOException e) {

            }
            // Close the HTTP connection
            try {
                if (httpClient != null) {
                    httpClient.close();
                }
            } catch (IOException e) {

            }
            
            ClientLogger.exiting("GraphQLAPIUtil", method);
        }
        return JWTToken;
    }

}