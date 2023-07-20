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
package cejavaapikey;
import java.io.*;
import java.util.*;

public class CEproperties
{
    // Define the property names that clients may make use of
    public static final String CE_URI = "CE_URI";
    public static final String APIC_TOKEN = "APIC_Token";
    public static final String APIC_TOKEN_URI = "APIC_URI";
    public static final String APIC_CLIENT_ID = "APIC_ClientId";
    public static final String APIC_CLIENT_SECRET = "APIC_ClientSecret";

    // Java properties class does the real work
    private static final String PROPERTIES_RESOURCE = "cejavaapikey.properties";
    private static Properties properties = new Properties ();

    // Constructor
    public CEproperties(String name)
    {
	if ( properties.isEmpty () )
        initializeProperties(name);
    }

    /**
     * @param String defaultValue
     * @param String property or key
     * @return the value for the key given or the defaultValue specified
     */
    public String get(String property, String defaultValue)
    {
        return properties.getProperty(property, defaultValue);
    }

    /**
     * @param String property or key
     * @return the value for the key given
     */
    public String get(String property)
    {
        return properties.getProperty(property);
    }
    
    // Open the properties file
    private synchronized void initializeProperties(String name)
    {
        if ( properties.isEmpty () )
        {
    	    File 				file;
    	    FileInputStream 	fis;
    	    InputStream 		inputStream = null;
    	    boolean 			found = false;
    	    String				fileName;

    	    // First try loading from the current working directory
    	    if( name.equals("") )
    	    	fileName = PROPERTIES_RESOURCE;
    	    else
    	    	fileName = name;
    	    file = new File(fileName);
    	    if( file.exists() )
    	    {
                try
                {
                    fis = new FileInputStream(file);
        	    found = true;
        	    inputStream = (InputStream)fis;
        	}
        	catch (IOException ex)
        	{
        	    System.err.println("IO exception CEjavaAPIkey.properties file CEproperties.initializeProperties");
        	    System.err.println(ex.getMessage());
        	}
    	    }

    	    // If that didn't work, try loading from classpath
    	    if( !found )
    	    	inputStream = CEproperties.class.getResourceAsStream("/" + fileName);

            try
            {
                properties.load(inputStream);
            }
            catch (IOException ioe)
            {
                RuntimeException runtimeException = new RuntimeException(ioe.getClass().getName() +
                                                      " in CEProperties while loading property resource " + fileName +
                                                      ".  Please make sure that " + fileName +
                                                      " is in your class path: " + ioe.getMessage());
                throw runtimeException;
            }
            catch (Exception e)
            {
                RuntimeException runtimeException = new RuntimeException(e.getClass().getName() +
                                                  " in CEProperties while loading property resource " + fileName +
                                                  ".  Please make sure that " + fileName +
                                                  " is in your class path: " +
                                                  e.getMessage());
                throw runtimeException;
            }

            // No penalty having empty properties file...
            if ( properties.isEmpty () )
                properties.put ( "dummy", "dummy" );
        }
    }
}
