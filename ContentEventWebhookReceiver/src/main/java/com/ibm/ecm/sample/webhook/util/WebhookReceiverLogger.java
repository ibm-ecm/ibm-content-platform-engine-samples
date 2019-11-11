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


import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

// Uncomment to add StringEscapeUtils for string filtering
//import org.apache.commons.lang.StringEscapeUtils;

/**
 * Collection of utility methods for handling logging with the Apache logger.
 * 
 * In a real-life application, it is a good idea to filter out newline and HTML
 * characters, as user provided strings could potentially contain fake log
 * messages (<a href="https://cwe.mitre.org/data/definitions/117.html">CWE-117:
 * Improper Output Neutralization for Logs</a>). The sample application has the
 * code commented out, as the response JSON from the GraphQL API logged in the
 * debug trace is easier to read with newline characters. If this application is
 * used as the bases for a real application, it would be good to edit the
 * {@code build.gradle} file to add the {@code commons-lang} library, import
 * {@code org.apache.commons.lang.StringEscapeUtils}, and uncomment the relevant
 * code in {@link #filter(String)}.
 */
public class WebhookReceiverLogger {
    private static final String SEPARATOR = ":";
    private static final String COMMA = ",";
    private static final Log LOGGER =
            LogFactory.getLog(Constants.LOGGER_RECEIVER);

    /**
     * Logs a message with the info log level. If multiple messages are
     * specified, the messages will be appended before being logged.
     * 
     * @param messages
     *            the set of messages to log
     */
    public static void info(String... messages) {
        if (LOGGER.isInfoEnabled()) {
            String completeMessage = appendMessages(messages);
            String filteredMessage = filter(completeMessage);
            LOGGER.info(filteredMessage);
        }
    }

    /**
     * Appends several message together delimited by commas
     * 
     * @param messages
     *            the messages to append together
     * @return a single string of the appended messages, delimited by commas
     */
    private static String appendMessages(String... messages) {
        String completeMessage;
        if (messages.length == 1) {
            completeMessage = messages[0];
        } else {
            StringBuffer sb = new StringBuffer();
            boolean firstMessage = true;
            for (String s : messages) {
                if (!firstMessage)
                    sb.append(COMMA);
                firstMessage = false;
                sb.append(s);
            }
            completeMessage = sb.toString();
        }
        return completeMessage;
    }

    /**
     * Logs a message with the warn log level. If multiple messages are
     * specified, the messages will be appended before being logged.
     * 
     * @param messages
     *            the set of messages to log
     */
    public static void warn(String... messages) {
        if (LOGGER.isWarnEnabled()) {
            String completeMessage = appendMessages(messages);
            String filteredMessage = filter(completeMessage);
            LOGGER.warn(filteredMessage);
        }
    }

    /**
     * Logs a message and a relevant exception that prompted the message with
     * the warn log level. If multiple messages are specified, the messages will
     * be appended before being logged.
     * 
     * @param message
     *            the message to log
     * @param t
     *            cause to log with the message
     */
    public static void warn(String message, Throwable t) {
        if (LOGGER.isWarnEnabled()) {
            String filteredMessage = filter(message);
            LOGGER.warn(filteredMessage, t);
        }
    }

    /**
     * Logs a message with the error log level. If multiple messages are
     * specified, the messages will be appended before being logged.
     * 
     * @param messages
     *            the set of messages to log
     */
    public static void error(String... messages) {
        if (LOGGER.isErrorEnabled()) {
            String completeMessage = appendMessages(messages);
            String filteredMessage = filter(completeMessage);
            LOGGER.error(filteredMessage);
        }
    }

    /**
     * Logs a message and a relevant exception that prompted the message with
     * the error log level. If multiple messages are specified, the messages
     * will be appended before being logged.
     * 
     * @param message
     *            the message to log
     * @param t
     *            cause to log with the message
     */
    public static void error(String message, Throwable t) {
        if (LOGGER.isErrorEnabled()) {
            String filteredMessage = filter(message);
            LOGGER.error(filteredMessage, t);
        }
    }

    /**
     * Logs a trace message when the code is about to throw an exception. The
     * exception will typically be caught by higher level code and logged as an
     * error but logging a trace message at the point when the exception is
     * thrown is a way to ensure that important information doesn't get lost if
     * the higher level code doesn't log the error for some reason. Tracing can
     * always be enabled to capture more information if the expected detail
     * isn't in the normal log.
     * 
     * @param msg
     *            Message to log with the exception
     * @param t
     *            Exception to log
     */
    public static void throwing(String msg, Throwable t) {
        if (LOGGER.isErrorEnabled()) {
            String filteredMessage = filter(msg);
            LOGGER.trace(filteredMessage, t);
        }
    }

    /**
     * Logs a message with the trace log level. If multiple messages are
     * specified, the messages will be appended before being logged.
     * 
     * @param messages
     *            the set of messages to log
     */
    public static void trace(String... messages) {
        if (LOGGER.isTraceEnabled()) {
            String completeMessage = appendMessages(messages);
            String filteredMessage = filter(completeMessage);
            LOGGER.trace(filteredMessage);
        }
    }

    /**
     * Logs a message with the debug log level. If multiple messages are
     * specified, the messages will be appended before being logged.
     * 
     * @param messages
     *            the set of messages to log
     */
    public static void debug(String... messages) {
        if (LOGGER.isDebugEnabled()) {
            String completeMessage = appendMessages(messages);
            String filteredMessage = filter(completeMessage);
            LOGGER.debug(filteredMessage);
        }
    }

    /**
     * Logs a message with the trace log level. The message will be used to
     * indicate the start of a given method from a given class
     * 
     * @param className
     *            Name of the class to which the logging method belongs
     * @param methodName
     *            Name of the method that was just started
     */
    public static void entering(String className, String methodName) {
        final String entryMsg = "Entering ";
        if (LOGGER.isTraceEnabled()) {
            LOGGER.trace(entryMsg + className + SEPARATOR + methodName);
        }
    }

    /**
     * Logs a message with the trace log level. The message will be used to
     * indicate the end of a given method from a given class
     * 
     * @param className
     *            Name of the class to which the logging method belongs
     * @param methodName
     *            Name of the method that just finished
     */
    public static void exiting(String className, String methodName) {
        final String entryMsg = "Exiting ";
        if (LOGGER.isTraceEnabled()) {
            LOGGER.trace(entryMsg + className + SEPARATOR + methodName);
        }
    }
    
    /**
     * If the StringEscapeUtils class is imported, this method filters out
     * newline and HTML characters. In the sample application, the filter code
     * is commented out, as the response JSON in the debug trace is easier to
     * read with newlines. A real application should filter logged messages to
     * prevent an attacker from injecting malicious content into the logs.
     * 
     * @param str
     *            The string to filter
     * @return An HTML-safe string with newlines replaced (if code is
     *         uncommented).
     */
    private static String filter(String str)
    {
        String filteredStr = str;
        // Uncomment to enable filtering of logged strings for ne
        /*if (str != null)
        {   // String is not null
            filteredStr = str.replace('\n', '_').replace('\r', '_');
            filteredStr = StringEscapeUtils.escapeHtml(filteredStr);
        }*/

        return filteredStr;
    }
}