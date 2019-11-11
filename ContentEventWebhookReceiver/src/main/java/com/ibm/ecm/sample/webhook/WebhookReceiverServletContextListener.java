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

package com.ibm.ecm.sample.webhook;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import javax.servlet.ServletContext;
import javax.servlet.ServletContextEvent;
import javax.servlet.ServletContextListener;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import com.ibm.ecm.sample.webhook.util.CSServerInfo;
import com.ibm.ecm.sample.webhook.util.Constants;
import com.ibm.ecm.sample.webhook.util.GraphQLAPIUtil;
import com.ibm.ecm.sample.webhook.util.GraphQLCallTemplate;
import com.ibm.ecm.sample.webhook.util.WebhookReceiverLogger;

/**
 * Handles logic for startup and shutdown of the Content Event Webhook Receiver
 * sample application. The startup (
 * {@link WebhookReceiverServletContextListener#contextInitialized(ServletContextEvent)}
 * ) will handle setup of the Webhook External Event Action and it
 * subscriptions, while the shutdown (
 * {@link WebhookReceiverServletContextListener#contextDestroyed(ServletContextEvent)}
 * ) will handle the teardown and cleanup of the event action and subscription
 * that was created, as well as any documents created as a part of driving the
 * example.
 * <p>
 * The logic in this class is primarily for demonstration purposes and for
 * helping to make a self-sufficient test application that leaves the system in
 * the original state. Some of this logic might be useful in a real world use
 * case, but is not necessarily required. When creating a real Webhook Receiver
 * application, feel free to remove unneeded sample code.
 */
public class WebhookReceiverServletContextListener implements
        ServletContextListener {

    /**
     * Handles setup for the Content Event Webhook Receiver sample application.
     * When the application starts up, the following events will occur.
     * 
     * <p>
     * <ol>
     * <li>Ping the Content Services GraphQL Server
     * <li>Create the Webhook External Event Action and subscription. Initially,
     * this event action and subscription will be subscribed to the
     * {@code CreationEvent} on the {@code WebhookClaim} class definition.
     * Later, the event action and subscription will be modified.
     * <li>Parse the response from the create call to get the external event
     * action ID for later cleanup
     * <li>Retrieve the Webhook External event Action and subscription so that
     * we can get the subscription ID. (Note: the previous create call will not
     * return information about the created subscription, which is why we need
     * to fetch it again. An alternative to this additional call is to specify a
     * specific ID for the subscription when creating it.)
     * <li>Parse the response from the query to get the subscription ID for
     * later cleanup
     * </ol>
     * <p>
     * Note that some of the logic below might not be realistic or desirable in
     * a real Webhook Receiver application. Some of the logic is included only
     * for demonstration purposes as an example and can be removed if it does
     * not make sense for an actual use case. In particular, in a real-life
     * use case scenario it might be better to keep the GUIDs for the event
     * action and subscriptions constant. In that case, more logic would need to
     * be added to check if the event action and subscriptions already exist
     * before creating them.
     * 
     * @param scEvent
     *            The context event object for startup, which allows us to get
     *            the servlet context object for saving data for later use.
     */
    @Override
    public void contextInitialized(ServletContextEvent scEvent) {
        String methodName = "contextInitialized";
        WebhookReceiverLogger.entering(this.getClass().getName(),
                methodName);
        ServletContext context = scEvent.getServletContext();

        // Ping the GraphQL server
        String objectStoreId = CSServerInfo.CS_SERVER_OBJECTSTORE;

        WebhookReceiverLogger.debug(
                "WebhookReceiverServletContextListener starting up-");
        WebhookReceiverLogger.debug("~~~~~~~~~~~~~~~~~~~~");

        WebhookReceiverLogger.debug("  =====+++++=====!!!!! "
                + "callGraphQLAPI ping with objectStoreId="
                + objectStoreId);
        String graphQLSchema = String.format(
                GraphQLCallTemplate.PING_CONTENTSERVICE_SERVER, objectStoreId);
        JSONObject jsonGraphQLResponse =
                GraphQLAPIUtil.callGraphQLAPI(graphQLSchema);

        // Handle errors in JSON, if any
        if (jsonGraphQLResponse.has("errors")) {
            JSONArray jsonResponseErrors = jsonGraphQLResponse
                    .getJSONArray("errors");

            // If there is an error, log response based on the first one
            if (jsonResponseErrors.length() > 0) {
                Object graphQLErrorObj = jsonResponseErrors.get(0);
                JSONObject graphQLError = new JSONObject(
                        graphQLErrorObj.toString());

                // Log the error
                String errorMessage = graphQLError.getString("message");
                WebhookReceiverLogger.error("Error contacting CPE",
                        errorMessage);
            }
        }

        // Create the event action and subscription
        String eventActionName = Constants.EVENTACTION_NAME;
        String eventActionDesc = Constants.EVENTACTION_DESCRIPTION;
        String webhookSecret = Constants.HMAC_CREDENTIAL_SECRET;
        String webhookReceiverURL = CSServerInfo.WEBHOOK_RECEIVER_URL;
        String webhookReceiverId = Constants.WEBHOOK_RECEIVER_REGISTRATION_ID;
        String subscriptionName = Constants.CREATE_EVENTSUBSCRIPTION_NAME;
        String subscriptionDesc = Constants.CREATE_EVENTSUBSCRIPTION_DESCRIPTION;
        WebhookReceiverLogger.debug("  =====+++++=====!!!!! "
                + "callGraphQLAPI eevCreateExternalEventAction "
                + "mutation with objectStoreId=" + objectStoreId,
                " eventActionName=" + eventActionName,
                " eventActionDesc=" + eventActionDesc,
                " webhookSecret=" + webhookSecret,
                " webhookReceiverURL=" + webhookReceiverURL,
                " webhookReceiverId=" + webhookReceiverId,
                " subscriptionName=" + subscriptionName,
                " subscriptionDesc=" + subscriptionDesc);
        graphQLSchema = String.format(
                GraphQLCallTemplate.CREATE_EVENTACTION_WITH_CLASSSUBSCRIPTION,
                objectStoreId, eventActionName, eventActionDesc, webhookSecret,
                webhookReceiverURL, webhookReceiverId, subscriptionName,
                subscriptionDesc);
        jsonGraphQLResponse = GraphQLAPIUtil.callGraphQLAPI(graphQLSchema);
        
        String eevExternalEventActionId = null;
        try {
            // Handle errors in JSON, if any
            if (jsonGraphQLResponse.has("errors")) {
                JSONArray jsonResponseErrors = jsonGraphQLResponse
                        .getJSONArray("errors");

                // If there is an error, log response based on the first one
                if (jsonResponseErrors.length() > 0) {
                    Object graphQLErrorObj = jsonResponseErrors.get(0);
                    JSONObject graphQLError = new JSONObject(
                            graphQLErrorObj.toString());

                    // Log the error
                    String errorMessage = graphQLError.getString("message");
                    WebhookReceiverLogger.error(
                            "Error creating Webhook External Event Action",
                            errorMessage);
                }
            }
            
            // Get EEV External Event Action ID
            JSONObject jsonResponseData =
                    jsonGraphQLResponse.getJSONObject("data");
            JSONObject jsonResponseEEVAction =
                    jsonResponseData.getJSONObject("eevCreateExternalEventAction");
            eevExternalEventActionId =
                    jsonResponseEEVAction.getString("id");

            WebhookReceiverLogger.info(
                    "Successfully created the Webhook External Event Action "
                            + "with ID=" + eevExternalEventActionId);
            context.setAttribute(Constants.EEV_EVENT_ACTION_ID_ATTR_KEY,
                    eevExternalEventActionId);

        } catch (JSONException je) {
            String errorMessage = "Unable to parse response JSON to get Webhook"
                    + " external event action ID";
            WebhookReceiverLogger.error(errorMessage, je);
        } catch (Exception e) {
            WebhookReceiverLogger.error(
                    "Unable to get ID for eevCreateExternalEventAction", e);
        }

        // Get the created subscriptions for later deletion
        if (eevExternalEventActionId != null) {
            // Retrieve the event action and associated subscription
            WebhookReceiverLogger.debug("  =====+++++=====!!!!! "
                    + "callGraphQLAPI fetch eevExternalEventAction "
                    + "query with objectStoreId=" + objectStoreId,
                    " eevExternalEventActionId=" + eevExternalEventActionId);
            graphQLSchema = String.format(
                    GraphQLCallTemplate.FETCH_EVENTACTION_WITH_CLASSSUBSCRIPTION,
                    objectStoreId, eevExternalEventActionId);
            jsonGraphQLResponse = GraphQLAPIUtil.callGraphQLAPI(graphQLSchema);
            
            List<String> subscriptionIdList =
                    Collections.synchronizedList(new ArrayList<String>());
            try {
                // Handle errors in JSON, if any
                if (jsonGraphQLResponse.has("errors")) {
                    JSONArray jsonResponseErrors = jsonGraphQLResponse
                            .getJSONArray("errors");

                    // If there is an error, log response based on the first one
                    if (jsonResponseErrors.length() > 0) {
                        Object graphQLErrorObj = jsonResponseErrors.get(0);
                        JSONObject graphQLError = new JSONObject(
                                graphQLErrorObj.toString());

                        // Log the error
                        String errorMessage = graphQLError.getString("message");
                        WebhookReceiverLogger.error(
                                "Error retrieving Webhook External Event subscriptions",
                                errorMessage);
                    }
                }

                // Get IDs of subscriptions for associated event action
                JSONObject jsonResponseData =
                        jsonGraphQLResponse.getJSONObject("data");
                JSONObject jsonResponseEEVAction =
                        jsonResponseData.getJSONObject("eevExternalEventAction");
                JSONObject jsonResponseSubscriptions =
                        jsonResponseEEVAction.getJSONObject("subscriptions");
                JSONArray jsonSubscriptionsArray =
                        jsonResponseSubscriptions.getJSONArray("subscriptions");
                
                // Add the IDs for each subscription to the array for later
                for(Object sub: jsonSubscriptionsArray) {
                    JSONObject s = new JSONObject(sub.toString());
                    String sId = s.getString("id");
                    subscriptionIdList.add(sId.toString());
                }

                WebhookReceiverLogger.info("List of Webhook subscription IDs="
                        + Arrays.toString(subscriptionIdList.toArray()));
                
                // Save External Event Action ID for update
                context.setAttribute(Constants.SUBSCRIPTION_ID_LIST_ATTR_KEY,
                        subscriptionIdList);

            } catch (JSONException je) {
                String errorMessage = "Unable to parse response JSON to get "
                        + "Webhook external event subscription IDs";
                WebhookReceiverLogger.error(errorMessage, je);
            } catch (Exception e) {
                WebhookReceiverLogger.error(
                        "Unable to get IDs from eevExternalEventAction", e);
            }
        }

        WebhookReceiverLogger.exiting(this.getClass().getName(),
                methodName);
    }

    /**
     * Handles teardown for the Content Event Webhook Receiver sample
     * application. When the application shuts down, the following events will
     * occur.
     * 
     * <p>
     * <ol>
     * <li>Delete the Webhook External Event Action created on startup and all
     * associated subscriptions. To do this with the GraphQL API, we need to do
     * an update mutation on the Webhook External Event Action to delete all
     * associated subscriptions first and then delete the event action. We are
     * able to do this all as batch to process both mutations in one call.
     * <li>Delete all instances of the {@code WebhookClaim} that were processed
     * by the Webhook Receiver sample application.
     * </ol>
     * <p>
     * Note that some of the logic below might not be realistic or desirable in
     * a real Webhook Receiver application. Some of the logic is included only
     * for demonstration purposes as an example and can be removed if it does
     * not make sense for an actual use case. In particular, in a real-life use
     * case scenario it might be better to not delete the event action and
     * subscription every time the application shuts down. Rather, it might be
     * better to move the cleanup to a separate call that can be used when
     * needed instead of every time the application shuts down.
     * 
     * @param scEvent
     *            The context event object for shutdown, which allows us to get
     *            the servlet context object so that we can get the data needed
     *            to cleanup desired objects.
     */
    @Override
    public void contextDestroyed(ServletContextEvent scEvent) {
        String methodName = "contextDestroyed";
        WebhookReceiverLogger.entering(this.getClass().getName(),
                methodName);
        ServletContext context = scEvent.getServletContext();

        String objectStoreId = CSServerInfo.CS_SERVER_OBJECTSTORE;

        WebhookReceiverLogger.debug(
                "WebhookReceiverServletContextListener shutting down-");
        WebhookReceiverLogger.debug("~~~~~~~~~~~~~~~~~~~~");

        // Get event action ID, subscription IDs, and document IDs
        String eevExternalEventActionId = (String) context.getAttribute(
                Constants.EEV_EVENT_ACTION_ID_ATTR_KEY);
        @SuppressWarnings("unchecked")
        List<String> subscriptionIdList = (List<String>) context.getAttribute(
                Constants.SUBSCRIPTION_ID_LIST_ATTR_KEY);
        @SuppressWarnings("unchecked")
        List<String> documentIdList = (List<String>) context.getAttribute(
                Constants.DOCUMENT_ID_LIST_ATTR_KEY);

        /*
         * Delete all subscriptions associated with the event action (if there
         * are any) first before the event action
         */
        if ((eevExternalEventActionId != null) && (subscriptionIdList != null)) {
            // Convert list of subscription IDs to a string
            String subIds = "";
            for(String subId : subscriptionIdList) {
                subIds = "\"" + subId + "\" ";
            }

            WebhookReceiverLogger.debug("  =====+++++=====!!!!! "
                    + "callGraphQLAPI batch eevUpdateExternalEventAction and "
                    + "eevDeleteExternalEventAction mutation with "
                    + "objectStoreId=" + objectStoreId,
                    " eevExternalEventActionId=" + eevExternalEventActionId,
                    " subscriptionIds=" + subIds);
            String graphQLSchema = String.format(
                    GraphQLCallTemplate.DELETE_EVENTACTION_SUBSCRIPTIONS,
                    objectStoreId, eevExternalEventActionId, subIds,
                    objectStoreId, eevExternalEventActionId);
            JSONObject jsonGraphQLResponse =
                    GraphQLAPIUtil.callGraphQLAPI(graphQLSchema);

            // Handle errors in JSON, if any
            if (jsonGraphQLResponse.has("errors")) {
                JSONArray jsonResponseErrors = jsonGraphQLResponse
                        .getJSONArray("errors");

                // If there is an error, log response based on the first one
                if (jsonResponseErrors.length() > 0) {
                    Object graphQLErrorObj = jsonResponseErrors.get(0);
                    JSONObject graphQLError = new JSONObject(
                            graphQLErrorObj.toString());

                    // Log the error
                    String errorMessage = graphQLError.getString("message");
                    WebhookReceiverLogger.error(
                            "Error deleting Webhook External Event Action and "
                                    + "subscriptions", errorMessage);
                }
            }

            WebhookReceiverLogger.info(
                    "Deleted the Webhook External Event Action with ID="
                            + eevExternalEventActionId);
            WebhookReceiverLogger.info("Deleted Webhook subscription IDs="
                    + Arrays.toString(subscriptionIdList.toArray()));
        }

        // Delete documents if we have an ID
        if ((documentIdList != null) && (documentIdList.size() > 0)) {
            // Iterate over each document and delete it
            for(String docId : documentIdList) {
                WebhookReceiverLogger.debug("  =====+++++=====!!!!! "
                        + "callGraphQLAPI deleteDocument "
                        + "mutation with objectStoreId=" + objectStoreId,
                        " docId=" + docId);
                String graphQLSchema = String.format(
                        GraphQLCallTemplate.DELETE_DOCUMENT,
                        objectStoreId, docId);
                JSONObject jsonGraphQLResponse =
                        GraphQLAPIUtil.callGraphQLAPI(graphQLSchema);

                // Handle errors in JSON, if any
                if (jsonGraphQLResponse.has("errors")) {
                    JSONArray jsonResponseErrors = jsonGraphQLResponse
                            .getJSONArray("errors");

                    // If there is an error, log response based on the first one
                    if (jsonResponseErrors.length() > 0) {
                        Object graphQLErrorObj = jsonResponseErrors.get(0);
                        JSONObject graphQLError = new JSONObject(
                                graphQLErrorObj.toString());

                        // Log the error
                        String errorMessage = graphQLError.getString("message");
                        WebhookReceiverLogger.error(
                                "Error deleting WebhookClaim documents",
                                errorMessage);
                    }
                }
                
                WebhookReceiverLogger.info(
                        "Deleted the WebhookClaim document with ID=" + docId);
            }
        }

        WebhookReceiverLogger.exiting(this.getClass().getName(),
                methodName);
    }
}
