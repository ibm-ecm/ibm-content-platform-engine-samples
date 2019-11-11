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

package com.ibm.ecm.sample.webhook.exception;

import javax.ws.rs.core.Response;
import javax.ws.rs.ext.ExceptionMapper;
import javax.ws.rs.ext.Provider;

/**
 * In the event that the Content Event Webhook External Event action callout to
 * the receiver sample application does not have the expected HMAC credential,
 * {@link com.ibm.ecm.sample.webhook.util.HMACAuthenticationFilter
 * HMACAuthenticationFilter} will throw a {@link HMACSecurityException}. This
 * class handles mapping that exception to a {@code UNAUTHORIZED} response code.
 * <p>
 * Note that handling for other uncaught exceptions can be added to this class,
 * or the servlet can handle the exception and return a response. It is up to
 * the implementor to decide which approach to take with every possible
 * exception.
 */
@Provider
public class WebhookReceiverExceptionMapper implements
        ExceptionMapper<Throwable> {

    @Override
    public Response toResponse(Throwable t) {
        Response.Status status = Response.Status.NOT_FOUND;
        if (t instanceof HMACSecurityException)
            status = Response.Status.UNAUTHORIZED;

        return Response.status(status).build();
    }
}