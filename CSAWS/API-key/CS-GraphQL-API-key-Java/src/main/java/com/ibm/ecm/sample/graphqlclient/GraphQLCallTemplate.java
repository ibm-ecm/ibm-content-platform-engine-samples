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
 * This class is used for keeping track of templates for various GraphQL calls.
 * See GraphQLCallTemplate.properties for the GraphQL call templates. Modify the
 * templates in the GraphQLCallTemplate.properties file to change the calls.
 * 
 * The GraphQL call templates can be freely modified, as long as the code that
 * uses the templates is also modified as necessary. 
 */
public class GraphQLCallTemplate {
    /**
     * Query for pinging the Content Services server. Parameters are bound to
     * this string in the following order:
     * <p>
     * <ul>
     * <li>Name or GUID of the object store
     * </ul>
     * <p>
     */
    public static final String PING_CONTENTSERVICE_SERVER;

    /**
     * Query the root folder of the object store
     * <p>
     * <ul>
     * <li>Name or GUID of the object store
     * </ul>
     * <p>
     **/
    public static final String QUERY_ROOT_FOLDER;
    
    /**
     * GraphQL call template properties, loaded from
     * {@code GraphQLCallTemplate.properties}
     */
    private static final Properties GRAPHQL_CALL_TEMPLATES;

    // Load the Content Services server info from CSServerInfo.properties
    static {
        GRAPHQL_CALL_TEMPLATES = new Properties();
        ClassLoader cl = GraphQLCallTemplate.class.getClassLoader();
        InputStream in = cl.getResourceAsStream(
                "com/ibm/ecm/sample/graphqlclient/GraphQLCallTemplate.properties");
        try {
            GRAPHQL_CALL_TEMPLATES.load(in);
            in.close();
        } catch (IOException e) {
            ClientLogger.error(
                    "Could not load GraphQLCallTemplate.properties", e);
        }
        
        // Load constants from CS_SERVER_INFO
        PING_CONTENTSERVICE_SERVER = getString("PING_CONTENTSERVICE_SERVER");
        QUERY_ROOT_FOLDER =
                getString("QUERY_ROOT_FOLDER");
    }
    
    /**
     * Get a property with the given key from GraphQLCallTemplate.properties.
     * The method returns null if the property is not found.
     * 
     * @param key
     *            the key of the property to get from
     *            GraphQLCallTemplate.properties
     * @return the value of the the property with the specified key, or null if
     *         there is no such property.
     */
    public static String getString(String key) {
        try {
            return GRAPHQL_CALL_TEMPLATES.getProperty(key);
        } catch (MissingResourceException e) {
            return null;
        }
    }
}
