/*
 * Licensed Materials - Property of IBM (c) Copyright IBM Corp. 2024 All Rights Reserved.
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

package com.ibm.ecm.sample.contentvalidation;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SocketChannel;
import java.security.PrivilegedExceptionAction;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;

import com.filenet.api.admin.*;
import com.filenet.api.authentication.UsernameCredentials;
import com.filenet.api.collection.*;
import com.filenet.api.constants.*;
import com.filenet.api.core.*;
import com.filenet.api.core.Domain;
import com.filenet.api.core.Factory;
import com.filenet.api.core.ObjectStore;
import com.filenet.api.engine.ContentValidator;
import com.filenet.api.engine.HandlerCallContext;
import com.filenet.api.util.Id;

/**
 * This provides a sample showing how to implement a Content Validator, a class
 * which can be hooked into the content ingestion code path allowing it to 
 * inspect content as it is uploaded and accept/reject it based on whatever
 * criteria is desired.
 *
 * This sample specifically submits the content to the ClamAV open source virus
 * checking service, but it shows the general pattern as well as the specifics
 * of that integration.
 *
 * Included in this class is the content validator itself plus code for
 * self-configuration of the validator against a specified object store.
 * Refer to the accompanying explanatory document for details.
 **/
public class ClamAVContentValidator implements ContentValidator
{
    private static String HOST_NAME_PROPERTY = "ClamAVHost";
    private static String PORT_PROPERTY = "ClamAVPort";
    private static String ACTION_CLASS_NAME = "ClamAVValidationAction";
    
    private static Id ACTION_INSTANCE_ID = new Id("{0d2483a2-1a2a-4b10-bd26-7a6d5bff1070}");
    
    private static Id HOST_TEMPLATE_ID = new Id("{dfc630ae-f2cb-43a3-aea4-938e70e2e83e}");
    private static Id PORT_TEMPLATE_ID = new Id("{144d4333-c11f-440a-8bb4-7d8f8d06f09d}");
    
    /**
     * Validates the acceptability of content being uploaded.
     *
     * The handler can accept or reject the content based on the retrieval
     * name or content type or by examining the content itself.
     *
     * @param action The <code>CmContentValidationAction</code> object which 
     *               configures the validator. Used in this case to read the
     *               host and port of the ClamAV service.
     * @param retrievalName The retrieval name specified by the client application
     *               creating the content element or null if no retrieval name
     *               was specified.
     * @param contentType The content type specified by the client application
     *               creating the content element or null if no content type
     *               was specified.
     * @param content An <code>InputStream</code> from which the validator can read
     *               the incoming content.
     *
     * @return Null if the content is acceptable or text giving the reason for unacceptibility.
     **/
      
    public String validateContent (
                        CmContentValidationAction action,
                        String retrievalName,
                        String contentType,
                        InputStream content )
    {
        String host = action.getProperties().getStringValue ( HOST_NAME_PROPERTY );
        int port = action.getProperties().getInteger32Value ( PORT_PROPERTY );
        
        return execute ( host, port, content );
    }

	private static final int CHUNK = 4096;
	private static final String INSTREAM = "zINSTREAM\0";
	private static final long MAX_CONTENT = 2147483648L;
    
	private static String execute ( String host, int port, InputStream is ) 
    {
        HandlerCallContext hcc = HandlerCallContext.getInstance();
        
		String resultText = "ClamAV Failure";
        
        if ( hcc.isDetailTraceEnabled () )
        {
            hcc.traceDetail("Connecting to ClamAV at " + host + ":" + port );
        }
        
		InetSocketAddress clamAVAddr = new InetSocketAddress( host, port );
		try (SocketChannel socketChannel = SocketChannel.open(clamAVAddr)) 
        {
			boolean isConnect = socketChannel.isConnected();
			if (isConnect) 
            {
				// Send command
				socketChannel.write((ByteBuffer) ByteBuffer.wrap(INSTREAM.getBytes()));

				// Send data, honouring 2Gb limit
                long totalSize = 0;
                
				ByteBuffer size = ByteBuffer.allocate(4);
				byte[] b = new byte[CHUNK];
				int chunk = is.read(b);
				while (chunk >= 0) 
                {
                    totalSize += chunk;
                    if ( totalSize > MAX_CONTENT )
                    {
                        hcc.logError ( "ClamAV maximum content size exceeded" );
                        return "ClamAV maximum content size exceeded";
                    }
					size.clear();
					size.putInt(chunk).flip();
					socketChannel.write(size);
					socketChannel.write(ByteBuffer.wrap(b, 0, chunk));
					chunk = is.read(b);
				}

				// Terminate by sending a zero
				size.clear();
				size.putInt(0).flip();
				socketChannel.write(size);

				// Read reply
				ByteBuffer data = ByteBuffer.allocate(1024);
				socketChannel.read(data);
				resultText = new String(data.array()).trim();
                
                if ( hcc.isDetailTraceEnabled() )
                {
                    hcc.traceDetail("ClamAV response: " + resultText);
                }
			}
		} 
        catch (IOException e) 
        {
            hcc.logError ( "ClamAV Exception " + e );
			return e.getMessage();
		}
        
		if (resultText.equals("stream: OK")) 
        {
            return null;
        }
        
        return resultText;
	}
    
    // ============== All of the code from here onwards is for self-configuration
    private static HashSet<String> options = new HashSet<String>();
    static
    {
        options.add ( "user" );
        options.add ( "password" );
        options.add ( "url" );
        options.add ( "objstore" );
        options.add ( "host" );
        options.add ( "port" );
    }
    
    /**
     * Self-configuration entrypoint.
     **/
    public static void main ( String[] args )
    {
        System.out.println ( "ClamAV content validator configuration tool" );
        
        HashMap<String,String> params = parseOptions ( args );
        
        String user = params.get("user");
        String password = params.get("password");
        
        System.out.println("Beginning operations as " + user);
        
        new UsernameCredentials ( user, password ).doAs (
                    new PrivilegedExceptionAction() 
                    {
                        public Object run()
                        {
                            configure ( params );
                            return null;
                        }
                    });
    }
    
    /**
     * Configuration method, executed in a doAs block.
     **/
    private static void configure ( HashMap<String,String> params )
    {
        String url = params.get("url");
		Connection conn = Factory.Connection.getConnection(url);
        Domain dom = Factory.Domain.getInstance(conn, null);
        String objectStoreName = params.get("objstore");
		ObjectStore objStore = Factory.ObjectStore.fetchInstance ( dom, objectStoreName, null );

        System.out.println("Successfully connected to object store " + objectStoreName );
        
        // Create the subclass of CmContentValidationAction with custom config properties
        createActionSubclass ( objStore );
        
        // Create a code module containing the code of this class
        CodeModule cm = createCodeModule ( objStore );
        
        // Create the action instance with the host and port value
        CmContentValidationAction action = createActionInstance (
                                                objStore,
                                                params.get("host"),
                                                params.get("port"),
                                                cm );
                                                
        // Apply the action to all storage areas
        Iterator<StorageArea> it = objStore.get_StorageAreas().iterator();
        while ( it.hasNext() )
        {
            StorageArea sa = it.next();
            sa.set_CmContentValidator ( action );
            sa.save ( RefreshMode.REFRESH );
            System.out.println("ClamAV validator applied to storage area " + sa.get_DisplayName() );
        }
    }
    
    /**
     * Creates the CmContentValidationAction subclass if it does not already exist.
     **/
    private static void createActionSubclass ( ObjectStore objStore )
    {
        ClassDefinition cd = null;
        try
        {
            cd = Factory.ClassDefinition.fetchInstance ( objStore, ACTION_CLASS_NAME, null );
            // Must exist already
            System.out.println ( "Fetched existing Class Definition " + ACTION_CLASS_NAME );
        }
        catch ( Exception e )
        {
            // Presumably does not exist, so create
            ClassDefinition cdBase = Factory.ClassDefinition.fetchInstance ( 
                                                                objStore, 
                                                                ClassNames.CM_CONTENT_VALIDATION_ACTION,
                                                                null );
            cd = cdBase.createSubclass();
            cd.set_SymbolicName ( ACTION_CLASS_NAME );
            LocalizedString ls = Factory.LocalizedString.createInstance ( objStore );
            ls.set_LocalizedText ( ACTION_CLASS_NAME );
            ls.set_LocaleName ( "en-us" );
            LocalizedStringList lsl = Factory.LocalizedString.createList();
            lsl.add ( ls );
            cd.set_DisplayNames ( lsl );
            cd.save ( RefreshMode.REFRESH );
            
            System.out.println ( "Successfully created Class Definition " + ACTION_CLASS_NAME );
        }
        
        // Make sure the required proeprties are present in the subclass.
        boolean update1 = addPropertyDefinition ( objStore, cd, HOST_TEMPLATE_ID, HOST_NAME_PROPERTY, TypeID.STRING);
        boolean update2 = addPropertyDefinition ( objStore, cd, PORT_TEMPLATE_ID, PORT_PROPERTY, TypeID.LONG);
        if ( update1 || update2 )
        {
            cd.save ( RefreshMode.REFRESH );
        }
        else
        {
            System.out.println("No updates required to class definition");
        }
    }

    /**
     * Add a custom property definition to the action subclass
     **/
    private static boolean addPropertyDefinition (
                        ObjectStore objStore,
                        ClassDefinition cd,
                        Id templateId,
                        String symbolicName, 
                        TypeID type )
    {
        PropertyDefinitionList pdl = cd.get_PropertyDefinitions();
        for ( int i = 0; i < pdl.size(); i++ )
        {
            PropertyDefinition pd = (PropertyDefinition)pdl.get(i);
            if ( pd.getProperties().isPropertyPresent ( PropertyNames.SYMBOLIC_NAME )
                 && pd.get_SymbolicName().equals ( symbolicName ) )
            {
                System.out.println("Property " + symbolicName + " already present");
                return false;
            }
        }
        
        // Property definition not already present. Create the template if not already.
        PropertyTemplate pt = createPropertyTemplate ( objStore, templateId, symbolicName, type );
        PropertyDefinition pd = pt.createClassProperty();
        pdl.add ( pd );
        System.out.println("Added property " + symbolicName);
        return true;
    }
    
    /**
     * Create a property template if not already existing.
     **/
    private static PropertyTemplate createPropertyTemplate ( 
                        ObjectStore objStore, 
                        Id templateId,
                        String symbolicName, 
                        TypeID type )
    {
        // May exist already
        try
        {
            return Factory.PropertyTemplate.fetchInstance ( objStore, templateId, null );
        }
        catch ( Exception e )
        {
        }
        
        PropertyTemplate pt = null;
        switch (type.getValue() )
        {
        case TypeID.STRING_AS_INT:
            pt = Factory.PropertyTemplateString.createInstance ( objStore, templateId );
            break;
            
        case TypeID.LONG_AS_INT:
            pt = Factory.PropertyTemplateInteger32.createInstance ( objStore, templateId );
            break;
        }
        
        pt.set_Cardinality ( Cardinality.SINGLE );
        pt.set_SymbolicName ( symbolicName );
        
        LocalizedString ls = Factory.LocalizedString.createInstance ( objStore );
        ls.set_LocalizedText ( symbolicName );
        ls.set_LocaleName ( "en-us" );
        LocalizedStringList lsl = Factory.LocalizedString.createList();
        lsl.add ( ls );
        pt.set_DisplayNames ( lsl );
        pt.save ( RefreshMode.REFRESH );
        System.out.println("Created new property template " + symbolicName );
        return pt;
    }
    
    /**
     * Create a code module containing the code of this class.
     **/
    private static CodeModule createCodeModule ( ObjectStore objStore )
    {
        try
        {
            CodeModule cm = Factory.CodeModule.createInstance ( objStore, ClassNames.CODE_MODULE );
            cm.getProperties().putValue ( "DocumentTitle", "ClamAV content validation handler code");
            String jarPath = ClamAVContentValidator.class.getProtectionDomain().getCodeSource().getLocation().getPath();
            System.out.println ( "ClamAV content validator code loaded from " + jarPath );
            ContentTransfer ct = Factory.ContentTransfer.createInstance ( objStore );
            File fjar = new File(jarPath);
            ct.set_RetrievalName ( fjar.getName() );
            ct.set_ContentType ( "application/java-archive" );
            ct.setCaptureSource ( new FileInputStream(fjar) );
            ContentElementList cel = Factory.ContentElement.createList();
            cel.add ( ct );
            cm.set_ContentElements ( cel );
            cm.checkin ( AutoClassify.DO_NOT_AUTO_CLASSIFY, CheckinType.MAJOR_VERSION );
            cm.save ( RefreshMode.REFRESH );
            System.out.println("Created code module " + cm.get_Id() );
            return cm;
        }
        catch ( Throwable t )
        {
            System.out.println("Exception in createCodeModule: " + t );
            System.exit(-1);
        }
        return null;
    }
    
    /**
     * Create the instance of the CmContentValidationAction subclass
     * needed to configure validation for storage areas, if it does not
     * already exist, or update it with a new code module reference and
     * potentially new host and port.
     **/
    private static CmContentValidationAction createActionInstance (
                    ObjectStore objStore,
                    String host,
                    String portString,
                    CodeModule cm )
    {
        CmContentValidationAction action = null;
        
        try
        {
            action = Factory.CmContentValidationAction.fetchInstance (
                                                            objStore,
                                                            ACTION_INSTANCE_ID,
                                                            null );
            System.out.println("Fetched existing content validation action");
        }
        catch ( Exception e )
        {
            // Doesn't already exist, create
            action = Factory.CmContentValidationAction.createInstance (
                                                            objStore,
                                                            ACTION_CLASS_NAME,
                                                            ACTION_INSTANCE_ID );
            System.out.println("Creaing content validation action");
        }
        
        action.set_CodeModule ( cm );
        action.set_ProgId ( ClamAVContentValidator.class.getName() );
        action.set_DisplayName ( "ClamAV Content Validation Action" );
        action.getProperties().putValue ( HOST_NAME_PROPERTY, host );
        try
        {
            action.getProperties().putValue ( PORT_PROPERTY, Integer.parseInt(portString) );
        }
        catch ( Throwable t )
        {
            System.out.println("Malformed port number " + portString );
            System.exit(-1);
        }
        action.save ( RefreshMode.REFRESH );
        System.out.println("Action properties set/updated" );
        return action;
    }
    
    /**
     * Parse the command line, generating a map of options to option value.
     **/
    private static HashMap<String,String> parseOptions ( String[] args )
    {
        HashMap<String,String> values = new HashMap<String,String>();
        
        int i = 0;
        while ( i < args.length )
        {
            String option = args[i].toLowerCase();
            if ( options.contains(option) )
            {
                if ( i+1 < args.length )
                {
                    values.put ( option, args[i+1] );
                }
                else
                {
                    System.out.println("No value supplied for option: " + args[i] );
                    System.exit(-1);
                }
            }
            else
            {
                System.out.println("Invalid option: " + args[i] );
                System.exit(-1);
            }
            i += 2;
        }

        // Make sure a value has been given for all the parameters
        Iterator<String> it = options.iterator();
        while ( it.hasNext() )
        {
            String option = it.next();
            if ( !values.containsKey ( option ) )
            {
                System.out.println("Missing option: " + option );
                System.exit(-1);
            }
        }
        return values;
    }
}
