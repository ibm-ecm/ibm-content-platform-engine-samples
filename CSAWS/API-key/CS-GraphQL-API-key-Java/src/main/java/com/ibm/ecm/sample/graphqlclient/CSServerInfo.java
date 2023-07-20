
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


import java.io.IOException;
import java.io.InputStream;
import java.util.MissingResourceException;
import java.util.Properties;

/**
 * This class is used for handling the Content Services server information,
 * including the GraphQL server URL and API connect info for the user that will
 * be used to connect to.
 */
public class CSServerInfo {

    /** Content Services GraphQL API URL */
    public static final String CS_SERVER_GRAPHQL_URL;
    /** Object Store */
    public static final String CS_SERVER_OBJECTSTORE;

    /** TOKEN for authentication */
    public static final String CS_SERVER_TOKEN;
    
    /** APIC API EndPoint, client id and client secret **/
    public static final String API_ENDPOINT;
    public static final String CLIENT_ID;
    public static final String CLIENT_SECRET;
    

    /**
     * Content Services server properties, loaded from
     * {@code CSServerInfo.properties}
     */
    private static final Properties CS_SERVER_INFO;

    // Load the Content Services server info from CSServerInfo.properties
    static {
        CS_SERVER_INFO = new Properties();
        ClassLoader cl = CSServerInfo.class.getClassLoader();
        InputStream in = cl.getResourceAsStream(
                "com/ibm/ecm/sample/graphqlclient/CSServerInfo.properties");
        try {
            CS_SERVER_INFO.load(in);
            in.close();
        } catch (IOException e) {
            ClientLogger.error(
                    "Could not load CSServerInfo.properties", e);
        }
        
        // Load constants from CS_SERVER_INFO
        CS_SERVER_GRAPHQL_URL = getString("CS_SERVER_GRAPHQL_URL");
        CS_SERVER_OBJECTSTORE = getString("CS_SERVER_OBJECTSTORE");
        CS_SERVER_TOKEN = getString("CS_SERVER_TOKEN");
        API_ENDPOINT = getString("API_ENDPOINT");
        CLIENT_ID = getString("CLIENT_ID");
        CLIENT_SECRET = getString("CLIENT_SECRET");
        
    }

    /**
     * Get a property with the given key from CSServerInfo.properties. The
     * method returns null if the property is not found.
     * 
     * @param key
     *            the key of the property to get from CSServerInfo.properties
     * @return the value of the the property with the specified key, or null if
     *         there is no such property.
     */
    public static String getString(String key) {
        try {
            return CS_SERVER_INFO.getProperty(key);
        } catch (MissingResourceException e) {
            return null;
        }
    }
}