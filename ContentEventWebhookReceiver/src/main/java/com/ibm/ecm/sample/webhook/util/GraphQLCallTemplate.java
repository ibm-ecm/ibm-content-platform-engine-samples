/*
 * Licensed Materials - Property of IBM (c) Copyright IBM Corp. 2019 All Rights Reserved.
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

package com.ibm.ecm.sample.webhook.util;

import java.io.IOException;
import java.io.InputStream;
import java.util.MissingResourceException;
import java.util.Properties;

/**
 * This class is used for keeping track of templates for various GraphQL calls.
 * See GraphQLCallTemplate.properties for the GraphQL call templates. Modify the
 * templates in the GraphQLCallTemplate.properties file to change the calls used
 * by the Content Event Webhook Receiver sample application. Variables in the
 * template are replaced with actual variables at runtime to create the actual
 * calls to the Content Services GraphQL API.
 * 
 * The GraphQL call templates can be freely modified, as long as the code that
 * uses the templates is also modified as necessary. In particular, the Event
 * action and subscription GUIDs could be changed to be hard-coded, which might
 * be preferable in a real-life scenario.
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
     * Mutation for creating Webhook external event action and subscription.
     * Parameters are bound to this string in the following order:
     * <p>
     * <ul>
     * <li>Name or GUID of the object store
     * <li>Webhook external event action name
     * <li>Webhook external event action description
     * <li>Webhook secret
     * <li>Webhook Receiver URL
     * <li>Webhook Receiver registration identifier
     * <li>Webhook external event subscription name
     * <li>Webhook external event subscription description
     * </ul>
     * <p>
     */
    public static final String CREATE_EVENTACTION_WITH_CLASSSUBSCRIPTION;
    
    /**
     * Query for retreiving the Webhook external event action and associated
     * subscriptions. Parameters are bound to this string in the following
     * order:
     * <p>
     * <ul>
     * <li>Name or GUID of the object store
     * <li>GUID of the external event action
     * </ul>
     * <p>
     **/
    public static final String FETCH_EVENTACTION_WITH_CLASSSUBSCRIPTION;
    
    /**
     * Mutation for updating an existing Webhook external event action and
     * subscription. Parameters are bound to this string in the following order:
     * <p>
     * <ul>
     * <li>Name or GUID of the object store
     * <li>GUID of the external event action
     * <li>New Webhook external event action name
     * <li>New Webhook external event subscription name
     * <li>New Webhook external event subscription description
     * <li>GUID of the Webhook external event subscription
     * </ul>
     * <p>
     **/
    public static final String UPDATE_EVENTACTION_WITH_CLASSSUBSCRIPTION;
    
    /**
     * Query for retrieving a document. Parameters are bound to this string in
     * the following order:
     * <p>
     * <ul>
     * <li>Name or GUID of the object store
     * <li>GUID of the document to fetch
     * </ul>
     * <p>
     **/
    public static final String GET_DOCUMENT;
    
    /**
     * Mutation for updating a document. Parameters are bound to this string in
     * the following order:
     * <p>
     * <ul>
     * <li>Name or GUID of the object store
     * <li>GUID of the document to modify
     * <li>Array of properties to modify
     * </ul>
     * <p>
     **/
    public static final String UPDATE_DOCUMENT;
    
    /**
     * Mutation for deleting a document. Parameters are bound to this string in
     * the following order:
     * <p>
     * <ul>
     * <li>Name or GUID of the object store
     * <li>GUID of the document to delete
     * </ul>
     * <p>
     **/
    public static final String DELETE_DOCUMENT;
    
    /**
     * Mutation for deleting existing Webhook external event action and
     * associated subscriptions. This mutation is a batch of two different
     * mutations. Parameters are bound to this string in the following order:
     * <p>
     * <ul>
     * <li>Name or GUID of the object store
     * <li>GUID of the external event action to delete
     * <li>List of subscription GUIDs to delete, each wrapped in double quotes
     * <li>GUID of the external event action to delete (second mutation)
     * <li>List of subscription GUIDs to delete, each wrapped in double quotes
     * (second mutation)
     * </ul>
     * <p>
     **/
    public static final String DELETE_EVENTACTION_SUBSCRIPTIONS;
    
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
                "com/ibm/ecm/sample/webhook/util/GraphQLCallTemplate.properties");
        try {
            GRAPHQL_CALL_TEMPLATES.load(in);
            in.close();
        } catch (IOException e) {
            WebhookReceiverLogger.error(
                    "Could not load GraphQLCallTemplate.properties", e);
        }
        
        // Load constants from CS_SERVER_INFO
        PING_CONTENTSERVICE_SERVER = getString("PING_CONTENTSERVICE_SERVER");
        CREATE_EVENTACTION_WITH_CLASSSUBSCRIPTION =
                getString("CREATE_EVENTACTION_WITH_CLASSSUBSCRIPTION");
        FETCH_EVENTACTION_WITH_CLASSSUBSCRIPTION =
                getString("FETCH_EVENTACTION_WITH_CLASSSUBSCRIPTION");
        UPDATE_EVENTACTION_WITH_CLASSSUBSCRIPTION =
                getString("UPDATE_EVENTACTION_WITH_CLASSSUBSCRIPTION");
        GET_DOCUMENT = getString("GET_DOCUMENT");
        UPDATE_DOCUMENT = getString("UPDATE_DOCUMENT");
        DELETE_DOCUMENT = getString("DELETE_DOCUMENT");
        DELETE_EVENTACTION_SUBSCRIPTIONS =
                getString("DELETE_EVENTACTION_SUBSCRIPTIONS");
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
