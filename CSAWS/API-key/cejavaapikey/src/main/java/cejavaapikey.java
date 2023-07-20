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
import cejavaapikey.CEproperties;

import java.security.PrivilegedExceptionAction;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import org.json.JSONObject;

import java.util.Iterator;
import java.util.Date;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.io.ByteArrayInputStream;

import com.filenet.api.core.*;
import com.filenet.api.authentication.OpenTokenCredentials;
import com.filenet.api.util.UserContext;
import com.filenet.api.util.Id;
import com.filenet.api.collection.AccessPermissionList;
import com.filenet.api.collection.ContentElementList;
import com.filenet.api.collection.ObjectStoreSet;
import com.filenet.api.constants.*;

class CEjavaAPIkey
{
    public static void main(String[] args) 
    {
        CEjavaAPIkey cejava = new CEjavaAPIkey();
        String	propsLocation = "";
        
        // Obtain our properties and test the connection
        CEproperties props = new CEproperties(propsLocation);
        boolean result = test_CEAPI_via_APIkey(props);
        System.exit(0);
    }
    
    static private boolean test_CEAPI_via_APIkey(CEproperties props)
    {
	// Get the connection parameters
	String token = props.get(props.APIC_TOKEN);
        String tokenUri = props.get(props.APIC_TOKEN_URI);
        String clientId = props.get(props.APIC_CLIENT_ID);
        String clientSecret = props.get(props.APIC_CLIENT_SECRET);

        // If an OIDC token was specified in the properties file, then just use it
        // Otherwise, obtain a token first from the API key endpoint
        if( token==null || token.length()<2 )
        {
            // Retrieve an OAuth token in exchange for an API key
            System.out.println(
              "Getting token from [" + tokenUri + "]\n" +
              "clientId=[" + clientId + "]\n" + "clientSecret=[" + clientSecret + "]");
            String resp = null;
            try {
                resp = getOAuthAccessToken(tokenUri, clientId, clientSecret);
            } 
            catch (Exception e) {
                System.out.println("Got an exception while attempting to obtain a token - exiting");
                e.printStackTrace();
                return false;
            }
            if( resp!= null )
            {
                try {
                    JSONObject jo = new JSONObject(resp);
                    if( jo!=null )
                        token = jo.getString("token");
                    if( token==null )
                    {
                        System.out.println("Failed to get a token from the APIC response - aborting");
                        return false;
                    }
                }
                catch (Exception e) {
                    System.out.println("JSON parsing exception with APIC response - aborting");
                    e.printStackTrace();
                    return false;
                }
            }
            else
            {
                System.out.println("Got a null response from APIC - aborting");
            }
        }
        else
            System.out.println("Using hard coded token:\n [" + token + "]");
        if( token==null )
            return false;
        
        // Pass the token into the CE API
        String ceURI = props.get(props.CE_URI);
        System.out.println(
              "Using CE endpoint: [" + ceURI + "]");
        OpenTokenCredentials otc = new OpenTokenCredentials(clientId, token, null);
		
	// Retrieve the Domain object
        PrivilegedExceptionAction<Domain> getDomainPEA = new PrivilegedExceptionAction<Domain>() 
        {
            public Domain run() throws Exception {
                try {
                    return Factory.Domain.fetchInstance(Factory.Connection.getConnection(ceURI), "", null);
                } 
                catch (Exception e) {
                     e.printStackTrace();
                    return null;
                }
            }
        };
        final Domain dom = otc.doAs(getDomainPEA);
        if( dom!=null )
	    System.out.println("Successfully connected to domain [" + dom.get_Name() + "]" );
        else
            System.out.println("Failed to retrieve domain object from CEWS - exiting");

	// Retrieve the ObjectStore object
        PrivilegedExceptionAction<ObjectStore> getOSPEA = new PrivilegedExceptionAction<ObjectStore>() 
        {
            public ObjectStore run() throws Exception {
                try {
                    ObjectStoreSet oss = dom.get_ObjectStores();
                    Iterator iter = oss.iterator();
                    return (ObjectStore)iter.next();
                } 
                catch (Exception e) {
                     e.printStackTrace();
                    return null;
                }
            }
        };
        final ObjectStore os = otc.doAs(getOSPEA);
        if( os!=null )
	    System.out.println("Successfully retrieved object store [" + os.get_Name() + "]" );
        else
            System.out.println("Failed to retrieve ObjectStore object from CEWS - exiting");

	// Create a new folder under the root node of the ObjectStore object
        PrivilegedExceptionAction<Folder> createFolderPEA = new PrivilegedExceptionAction<Folder>() 
        {
            public Folder run() throws Exception {
                try {
                    Folder root = os.get_RootFolder();
		    DateFormat dateFormat = new SimpleDateFormat("YYYY_MM_dd_HH_mm_SS");
		    Date now = new Date();
                    String fName = dateFormat.format(now);
                    Folder newFolder = root.createSubFolder(fName);
                    newFolder.save(RefreshMode.REFRESH);
                    return newFolder;
                } 
                catch (Exception e) {
                     e.printStackTrace();
                    return null;
                }
            }
        };
        final Folder fld = otc.doAs(createFolderPEA);
        if( fld!=null )
	    System.out.println("Successfully created folder [" + fld.get_FolderName() + "]" );
        else
            System.out.println("Failed to create a folder via CEWS - exiting");

	// Create a new doc (no content) under the folder created above
        PrivilegedExceptionAction<Document> createDocPEA = new PrivilegedExceptionAction<Document>() 
        {
            public Document run() throws Exception {
                try {
		    DateFormat dateFormat = new SimpleDateFormat("YYYY_MM_dd_HH_mm_SS");
		    Date now = new Date();
                    String dName = dateFormat.format(now);
                    Id id = Id.createId();
                    Id vsId = Id.createId();
                    Document doc = Factory.Document.createInstance(os, null, id, vsId, null);
                    doc.getProperties().putValue("DocumentTitle", dName);
                    doc.save(RefreshMode.REFRESH);

                    // And file it in our folder
                    ReferentialContainmentRelationship rcr =
                      fld.file(doc, AutoUniqueName.AUTO_UNIQUE, dName, DefineSecurityParentage.DO_NOT_DEFINE_SECURITY_PARENTAGE);
                    rcr.save(RefreshMode.NO_REFRESH);
                    return doc;
                } 
                catch (Exception e) {
                     e.printStackTrace();
                    return null;
                }
            }
        };
        final Document doc1 = otc.doAs(createDocPEA);
        if( doc1!=null )
	    System.out.println("Successfully created document without content [" + doc1.getProperties().getStringValue("DocumentTitle") + "]" );
        else
            System.out.println("Failed to create a document without content via CEWS - exiting");

	// Create a 2nd new doc (with content) under the folder created above
        PrivilegedExceptionAction<Document> createDoc2PEA = new PrivilegedExceptionAction<Document>() 
        {
            public Document run() throws Exception {
                try {
		    DateFormat dateFormat = new SimpleDateFormat("YYYY_MM_dd_HH_mm_SS");
		    Date now = new Date();
                    String dName = dateFormat.format(now) + "_withContent";
                    Id id = Id.createId();
                    Id vsId = Id.createId();
                    Document doc = Factory.Document.createInstance(os, null, id, vsId, null);
                    doc.getProperties().putValue("DocumentTitle", dName);

                    //  Add some content and save
                    ContentTransfer transfer = Factory.ContentTransfer.createInstance();
                    ByteArrayInputStream input = new ByteArrayInputStream("Some test data.".getBytes());
                    transfer.setCaptureSource(input);
                    transfer.set_RetrievalName(dName);
                    ContentElementList elements = Factory.ContentElement.createList();
                    elements.add(transfer);
                    doc.set_ContentElements(elements);
                    doc.save(RefreshMode.REFRESH);

                    // And file it in our folder
                    ReferentialContainmentRelationship rcr =
                      fld.file(doc, AutoUniqueName.AUTO_UNIQUE, dName, DefineSecurityParentage.DO_NOT_DEFINE_SECURITY_PARENTAGE);
                    rcr.save(RefreshMode.NO_REFRESH);
                    return doc;
                } 
                catch (Exception e) {
                     e.printStackTrace();
                    return null;
                }
            }
        };
        final Document doc2 = otc.doAs(createDoc2PEA);
        if( doc2!=null )
	    System.out.println("Successfully created document with content [" + doc2.getProperties().getStringValue("DocumentTitle") + "]" );
        else
            System.out.println("Failed to create a document with content via CEWS - exiting");

	return true;
    }


    /**
     * Get OAuth access token
     * 
     * @param tokenUri       APIC token URI
     * @param clientId       Service user name associated with the API key
     * @param clientSecret   The actual API key value
     */
    private static String getOAuthAccessToken(String tokenUri, String clientId, String clientSecret) throws Exception {

        // Build a request and send it off
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
              .uri(URI.create(tokenUri))
              .header("content-type", "application/json")
              .header("X-IBM-Client-Id", clientId)
              .header("X-IBM-Client-Secret", clientSecret)
              .GET()
              .build();
        HttpResponse<String> response = HttpClient.newBuilder()
               .build()
               .send(request, java.net.http.HttpResponse.BodyHandlers.ofString());
        String responseBody = response.body();
        System.out.println("Response=[" + responseBody + "]");
        if( response.statusCode()>=400 )
        {
            System.out.println("Failed to retrieve an OIDC token from APIC.  Status code=" + response.statusCode());
            return null;
        }
        else
            return responseBody;
    }
}

