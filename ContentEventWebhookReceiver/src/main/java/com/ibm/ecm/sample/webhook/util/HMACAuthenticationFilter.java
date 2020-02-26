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

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.security.SignatureException;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import javax.ws.rs.ext.Provider;
import javax.ws.rs.ext.ReaderInterceptor;
import javax.ws.rs.ext.ReaderInterceptorContext;
import javax.xml.bind.DatatypeConverter;

import com.ibm.ecm.sample.webhook.exception.HMACSecurityException;

/**
 * The {@code HMACAuthenticationFilter} class implements the
 * {@link javax.ws.rs.ext.ReaderInterceptor ReaderInterceptor} class, which
 * combined with the {@code @Provider} annotation allows this class to
 * automatically intercept any requests before they are accepted by the REST
 * servlet.
 * <p>
 * This class handles the validation of the HMAC credentials that are passed by
 * the Content Event Webhook External Event Action. On the Content Platform
 * Engine side, the External Event Action has an External Receiver Credentials
 * (EevEventReceiverCredentials) property, where the user specifies the
 * credential type. In Content Platform Engine 5.5.4, only HMAC credentials and
 * the {@code HmacSHA1} algorithm are supported. The user must specify a secret
 * value in the External Receiver Credentials that matches the secret value on
 * the External Event Receiver application. This secret value is then used as a
 * cryptographic key along with the External Event action payload to generate an
 * HMAC value.
 * <p>
 * The HMC credential serves two purposes:
 * <p>
 * <ol>
 * <li>Verify that the External Event Action callout is meant specifically for
 * this Receiver application and not a different Receiver application
 * <li>Validate that the request has not been tampered with and is coming from
 * the trusted sender (the Content Platform Engine server)
 * </ol>
 * <p>
 */
@Provider
public class HMACAuthenticationFilter implements ReaderInterceptor {
    private static final String HMAC_CREDENTIALS_HEADER = "hmac";
    private static final String HMAC_SHA1_ALGORITHM = "HmacSHA1";

    /**
     * This method is the implementation of the
     * {@link javax.ws.rs.ext.ReaderInterceptor#aroundReadFrom(ReaderInterceptorContext)
     * aroundReadFrom} method. This is the method that will be used to intercept
     * calls before they are handled by the REST servlet.
     * <p>
     * Verifies the External Event action call has a valid HMAC by comparing it
     * to an independently and dynamically generated HMAC. As long as the
     * payload has not been tampered with or altered, the secret key is the same
     * on both the External Event action and the Receiver application, and the
     * same algorithm is used, the HMAC keys should be the same.
     * <p>
     * The sample application uses the constant {@code HMAC_CREDENTIALS_HEADER}
     * for the HMAC validation and also sets the same secret on the External
     * Event Action that is created/configured on startup of the application.
     * 
     * @param ctx
     *            Interceptor context, automatically passed by the interceptor
     *            infrastructure.
     * @return {@code ctx.proceed()} object, which is needed to proceed to the
     *         next interceptor for the call, unless an exception is thrown.
     * @throws IOException
     *             if there is a problem reading the payload from the
     *             intercepted call
     */
    public Object aroundReadFrom(ReaderInterceptorContext ctx)
            throws IOException {
        String methodName = "aroundReadFrom";
        WebhookReceiverLogger.entering(this.getClass().getName(), methodName);
        
        // Get HMAC header from Webhook event action call
        String hmacHeaderValue = ctx.getHeaders().getFirst(
                HMAC_CREDENTIALS_HEADER);
        WebhookReceiverLogger.trace("Headers = " + ctx.getHeaders());
        byte[] requestPayloadBytes = convertInputStreamIntoByteArrayOutputStream(
                ctx.getInputStream()).toByteArray();
        
        // Verify HMAC header value
        boolean authenticated = verifyHMACHeader(hmacHeaderValue,
                requestPayloadBytes);
        if (!authenticated) {
            throw new HMACSecurityException("hmacHeaderValue did not match ");
        }
        ctx.setInputStream(new ByteArrayInputStream(requestPayloadBytes));
        
        WebhookReceiverLogger.exiting(this.getClass().getName(), methodName);
        return ctx.proceed();
    }

    /**
     * Verifies that the HMAC credential passed by the External Event call
     * matches an HMAC credential generated from the Secret Credential and the
     * External Event action call payload. As long as the secret and algorithm
     * on the External Event action and the application match, the HMACs should
     * match.
     * 
     * @param hmacHeaderValue
     *            HMAC from External Event action call to validate
     * @param requestPayloadBytes
     *            A byte array representation of the JSON payload from the
     *            External Event action call. The HMAC is dynamically generated
     *            from this byte array and the Secret Credential
     * @return true if the External Event action call HMAC matches the
     *         dynamically generated HMAC, or false if they do not match.
     */
    private boolean verifyHMACHeader(String hmacHeaderValue,
            byte[] requestPayloadBytes) {
        String methodName = "verifyHMACHeader";
        WebhookReceiverLogger.entering(this.getClass().getName(), methodName);
        boolean validated = false;

        String requestPayload = new String(requestPayloadBytes);
        WebhookReceiverLogger.trace("hmacHeaderValue=" + hmacHeaderValue,
                " requestPayload=" + requestPayload);
        String hmacComputed = null;
        
        try {
            if (requestPayload != null) {
                hmacComputed = calculateHMAC(requestPayload,
                        Constants.HMAC_CREDENTIAL_SECRET);
            }
            // Verify HMAC header value and computed HMAC are equal and not null
            validated = ((hmacComputed != null) && (hmacHeaderValue != null)
                    && hmacComputed.equals(hmacHeaderValue));
            WebhookReceiverLogger.trace(
                    "hmacComputed=" + hmacComputed,
                    " hmacHeaderValue=" + hmacHeaderValue,
                    " hmacComputed.equals(hmacHeaderValue)="
                            + hmacComputed.equals(hmacHeaderValue));
        } catch (Exception e) {
            WebhookReceiverLogger.error(
                    "Exception thrown when attempting to validate HMAC", e);
        }

        WebhookReceiverLogger.exiting(this.getClass().getName(), methodName);
        return validated;
    }

    /**
     * Reads the input stream and dumps the content into a byte array
     * 
     * @param inputStream
     *            stream to dump into byte array
     * @return byte array with contents of the input stream
     * @throws IOException
     *             if there is a problem reading from the input stream or with
     *             the output stream
     */
    private ByteArrayOutputStream convertInputStreamIntoByteArrayOutputStream(
            InputStream inputStream) throws IOException {
        // Protect against null value for inputStream
        if (inputStream == null) {
            return null;
        }

        byte[] byteChunk = new byte[1024];
        int length = -1;
        ByteArrayOutputStream baos = new ByteArrayOutputStream();

        try {
            // Read input stream and write to the Byte Array output stream
            while ((length = inputStream.read(byteChunk)) != -1) {
                baos.write(byteChunk, 0, length);
            }
            baos.flush();
        } finally {
            inputStream.close();
            baos.close();
        }
        return baos;
    }

    /**
     * Calculates an HMAC for a given string and key.
     * 
     * @param data
     *            String to calculate an HMAC for
     * @param key
     *            A secret cryptographic key to use to calculate HMAC
     * @return HMAC for the given string and key
     * @throws SignatureException
     *             if the HMAC is unable to be generated
     * @throws NoSuchAlgorithmException
     *             if no Provider supports the {@code HmacSHA1} algorithm
     * @throws InvalidKeyException
     *             if the given key is inappropriate for initializing the HMAC.
     */
    private String calculateHMAC(String data, String key)
            throws SignatureException, NoSuchAlgorithmException,
            InvalidKeyException {
        SecretKeySpec signingKey = new SecretKeySpec(key.getBytes(),
                HMAC_SHA1_ALGORITHM);
        Mac mac = Mac.getInstance(HMAC_SHA1_ALGORITHM);
        mac.init(signingKey);
        return toBase64(mac.doFinal(data.getBytes()));
    }

    /**
     * Converts an array of bytes into a Base 64 encoded string.
     * 
     * @param bytes
     *            Array of bytes to convert
     * @return A base 64 encoded string representation of the provided byte
     *         array
     */
    private static String toBase64(byte[] bytes) {
        return DatatypeConverter.printBase64Binary(bytes);
    }
}