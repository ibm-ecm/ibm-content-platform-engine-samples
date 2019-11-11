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
 * This class is used for handling the Content Services server information,
 * including the GraphQL server URL and login credentials for the user that will
 * be used to configure the Content Event Webhook and handle callback requests
 * to process the document that triggered the Webhook's subscription.
 * 
 * Make sure to change the information set in CSServerInfo.properties to have
 * the appropriate Content Services GraphQL server URL and CPE admin user to use
 * for setting up the Content Event Webhook event action and subscription and
 * callback logic.
 * 
 * Note that user credentials are stored in clear text in
 * {@code CSServerInfo.properties} for simplicity of setup of this sample
 * Content Event Webhook Receiver application. In a production environment, a
 * different approach should be used to store, encrypt, and retrieve the user
 * credentials.
 */
public class CSServerInfo {

    /** Content Services GraphQL API URL */
    public static final String CS_SERVER_GRAPHQL_URL;
    /** Object Store for Content Event Webhook Receiver sample */
    public static final String CS_SERVER_OBJECTSTORE;
    /**
     * Content Event Webhook Receiver URL.
     */
    public static final String WEBHOOK_RECEIVER_URL;
    /**
     * CPE/Content Services user. User must have full control on the Object
     * Store configured for the Content Event Webhook
     */
    public static final String CS_SERVER_USERNAME ;
    /** CPE/Content Services password. */
    public static final String CS_SERVER_PASSWORD;

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
                "com/ibm/ecm/sample/webhook/util/CSServerInfo.properties");
        try {
            CS_SERVER_INFO.load(in);
            in.close();
        } catch (IOException e) {
            WebhookReceiverLogger.error(
                    "Could not load CSServerInfo.properties", e);
        }
        
        // Load constants from CS_SERVER_INFO
        CS_SERVER_GRAPHQL_URL = getString("CS_SERVER_GRAPHQL_URL");
        CS_SERVER_OBJECTSTORE = getString("CS_SERVER_OBJECTSTORE");
        WEBHOOK_RECEIVER_URL = getString("WEBHOOK_RECEIVER_URL");
        CS_SERVER_USERNAME = getString("CS_SERVER_USERNAME");
        CS_SERVER_PASSWORD = getString("CS_SERVER_PASSWORD");
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
