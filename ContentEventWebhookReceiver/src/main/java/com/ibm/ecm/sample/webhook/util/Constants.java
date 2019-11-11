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

/**
 * General constants for the Content Event Webhook Receiver sample application,
 * including constants to use for the Content Event Webhook External Event
 * Actions and Subscriptions created by this sample application, as well as
 * the key names for {@code ServletContext} attributes for sharing data across
 * the sample application and the package name to use for logging.
 */
public class Constants {

    // Event action and subscription names and descriptions
    public static final String CREATE_EVENTSUBSCRIPTION_NAME =
            "WebhookReceiverDocumentCreationSub";
    public static final String CREATE_EVENTSUBSCRIPTION_DESCRIPTION =
            "Content Event Sample Webhook Receiver Document Creation Subscription";
    public static final String UPDATE_EVENTSUBSCRIPTION_NAME =
            "WebhookReceiverDocumentUpdateSub";
    public static final String UPDATE_EVENTSUBSCRIPTION_DESCRIPTION =
            "Content Event Sample Webhook Receiver Document Update Subscription";
    public static final String EVENTACTION_NAME =
            "WebhookReceiverDocumentEventAction";
    public static final String EVENTACTION_DESCRIPTION =
            "Content Event Sample Webhook Receiver Document Event Action";

    // Webhook Event Action properties
    public static final String WEBHOOK_RECEIVER_REGISTRATION_ID = "ceswr";
    public static final String HMAC_CREDENTIAL_SECRET =
            "eb497ac4891d6009d8ef601bfdf6c3f5";
    
    /*
     * ServletContext attribute key constants, which are used to share data
     * across classes
     */
    public static final String EVENTS_JSON_ATTR_KEY = "EVENTS_JSON";
    public static final String EEV_EVENT_ACTION_ID_ATTR_KEY = "EEV_ACTION_ID";
    public static final String SUBSCRIPTION_ID_LIST_ATTR_KEY = "SUB_ID_LIST";
    public static final String DOCUMENT_ID_LIST_ATTR_KEY = "DOC_ID_LIST";
    
    // Logging constants
    public static final String LOGGER_RECEIVER = "com.ibm.ecm.sample.webhook";

}
