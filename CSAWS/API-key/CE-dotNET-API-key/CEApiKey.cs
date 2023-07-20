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
using System;
using System.IO;
using System.Collections;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using Newtonsoft.Json;
using FileNet.Api.Constants;
using FileNet.Api.Core;
using FileNet.Api.Collection;
using FileNet.Api.Authentication;
using FileNet.Api.Util;
//using static System.Net.Mime.MediaTypeNames;
//using System.Security.Claims;
//using System.Runtime.Remoting.Messaging;

namespace CEApiKey
{
    class CEApiKeySample
    {
        static async Task Main(string[] args)
        {
            CEApiKeySample ceapikeysample = new CEApiKeySample();
            string propsLocation = "C:\\cpedotnetapp\\TestOrbitApikey\\ceapikey.properties";

            // Obtain our properties and test the connection
            CEProperties props = new CEProperties(propsLocation);
            bool result = await Test_CEAPI_via_APIkey(props);
        }

        static private async Task<bool> Test_CEAPI_via_APIkey(CEProperties props)
        {
            // Get the connection parameters
            string token = props.Get(CEProperties.APIC_TOKEN);
            string tokenUri = props.Get(CEProperties.APIC_TOKEN_URI);
            string clientId = props.Get(CEProperties.APIC_CLIENT_ID);
            string clientSecret = props.Get(CEProperties.APIC_CLIENT_SECRET);
            string ceURI = props.Get(CEProperties.CE_URL);
            string ceContentPath = props.Get(CEProperties.CE_CONTENT_PATH);
            string ceDownloadFolder = props.Get(CEProperties.CE_DOWNLOAD_FOLDER);
            // If an OIDC token was specified in the properties file, then just use it
            // Otherwise, obtain a token first from the API key endpoint
            if (string.IsNullOrEmpty(token) || token.Length < 2)
            {
                // Retrieve an OAuth token in exchange for an API key
                Console.WriteLine($"Getting token from [{tokenUri}]\n" +
                    $"clientId=[{clientId}]\n" +
                    $"clientSecret=[{clientSecret}]");
                string resp = null;
                try
                {
                    resp = await GetOAuthAccessToken(tokenUri, clientId, clientSecret);
                }
                catch (Exception e)
                {
                    Console.WriteLine("Got an exception while attempting to obtain a token - exiting");
                    Console.WriteLine(e.Message);
                    return false;
                }
                if (!string.IsNullOrEmpty(resp))
                {
                    var jsonObject = JsonConvert.DeserializeObject<dynamic>(resp);
                    if (jsonObject != null)
                    {
                        token = jsonObject.token;
                    }
                    if (string.IsNullOrEmpty(token))
                    {
                        Console.WriteLine("Failed to get a token from the APIC response - aborting");
                        return false;
                    }
                }
                else
                {
                    Console.WriteLine("Got a null response from APIC - aborting");
                }
            }
            else
                Console.WriteLine($"Using hard coded token:\n [{token}]");
            if (string.IsNullOrEmpty(token))
                return false;

            // Pass the token into the CE API
            OpenTokenCredentials otc = new OpenTokenCredentials(clientId, token, null);
            
            Console.WriteLine("\nMake Connection to Content Platform Engine");
            Console.WriteLine($"ceURI=[{ceURI}]");
            try
            {
                // Get client context.
                IConnection conn = Factory.Connection.GetConnection(ceURI);
                OpenTokenCredentials creds = new OpenTokenCredentials(clientId, token, null);
                ClientContext.SetProcessCredentials(creds);

                // Get default domain.
                IDomain domain = Factory.Domain.FetchInstance(conn, null, null);
                Console.WriteLine("Domain: " + domain.Name);
                Console.WriteLine("Connection to Content Platform Engine successful");
                // Get object stores for domain.
                foreach (IObjectStore os in domain.ObjectStores)
                {
                    Console.WriteLine("\nObject Store: " + os.Name);
                    var root = os.RootFolder;
                    // Get current time.   
                    DateTime currentDate = DateTime.Now;
                    String fName = currentDate.ToString("yyyy_MM_dd_HH_mm_ss");
                    var folder = root.CreateSubFolder(fName);
                    folder.Save(RefreshMode.REFRESH);

                    if (folder != null)
                        Console.WriteLine("Successfully created folder [" + folder.FolderName + "]");
                    else
                    {
                        Console.WriteLine("Failed to create a folder via CEWS");
                    }
                    // create a document from content file specified in the ceapikey.properties file
                    IDocument doc = CreateDocumentFromFile(os, folder, ceContentPath);

                    // retrieve content of the document
                    TestContentRetrieval(doc, ceDownloadFolder);

                }
                //Console.WriteLine("Connection to Content Platform Engine successful");
            }
            catch (Exception exc)
            {
                Console.WriteLine(exc.ToString());
            }
            return true;
        }

        /**
         * Get OAuth access token
         *
         * @param tokenUri       APIC token URI
         * @param clientId       Service user name associated with the API key
         * @param clientSecret   The actual API key value
         */
        private static async Task<string> GetOAuthAccessToken(string tokenUri, string clientId, string clientSecret)
        {
            // Build a request and send it off
            using (var client = new HttpClient())
            {
                client.DefaultRequestHeaders.Accept.Clear();
                client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
                client.DefaultRequestHeaders.Add("X-IBM-Client-Id", clientId);
                client.DefaultRequestHeaders.Add("X-IBM-Client-Secret", clientSecret);

                var response = await client.GetAsync(tokenUri);
                if (response.IsSuccessStatusCode)
                {
                    var responseBody = await response.Content.ReadAsStringAsync();
                    Console.WriteLine("Response=[" + responseBody + "]");
                    return responseBody;
                }
                else
                {
                    Console.WriteLine("Failed to retrieve an OIDC token from APIC.  Status code=" + response.StatusCode);
                    return null;
                }
            }
        }

        private static IDocument CreateDocumentFromFile(IObjectStore os, IFolder folder, string contentPath)
        {
            Console.WriteLine("\nCreate a document with content");
            //Console.WriteLine(" Create a document and set content elements");
            IContentTransfer ct = Factory.ContentTransfer.CreateInstance(os);
            String fileName = Path.GetFileName(contentPath);
            String contentType = "text/plain";
            if (fileName.EndsWith(".class"))
            {
                contentType = ("application/java-byte-code");
            }
            else if (fileName.EndsWith(".zip") || fileName.EndsWith(".jar"))
            {
                contentType = ("application/x-zip-compressed");
            }
            else if (fileName.EndsWith(".mp4"))
            {
                contentType = ("video/mp4");
            }
            ct.ContentType = contentType;
            ct.SetCaptureSource(new FileStream(contentPath, FileMode.Open, FileAccess.Read));
            ct.RetrievalName = Path.GetFileName(contentPath);
            IDependentObjectList cel = Factory.ContentElement.CreateList();
            cel.Add(ct);
            //Console.WriteLine(" Creates an IDocument instance");
            IDocument doc = Factory.Document.CreateInstance(os, ClassNames.DOCUMENT);
            doc.ContentElements = (IContentElementList)cel;
            //Console.WriteLine(" Check in IDocument instance");
            doc.Checkin(AutoClassify.DO_NOT_AUTO_CLASSIFY, CheckinType.MAJOR_VERSION);
            doc.Save(RefreshMode.REFRESH);

            //Console.WriteLine(" Try retrieving the document from Id");
            String docId = doc.Id.ToString();
            doc = null;
            doc = Factory.Document.FetchInstance(os, docId, null);
            Console.WriteLine("Document with content created successfully: " + docId);

            Console.WriteLine("File the Document in folder: " + folder.Name);
            IReferentialContainmentRelationship rcr = folder.File(doc, AutoUniqueName.AUTO_UNIQUE, Path.GetFileName(contentPath), DefineSecurityParentage.DO_NOT_DEFINE_SECURITY_PARENTAGE);
            rcr.Save(RefreshMode.NO_REFRESH);
            return doc;
        }

        private static void TestContentRetrieval(IDocument doc, String ceDownloadFolder)
        {
            Console.WriteLine("\nDownload content elements from a dcoument");
            IContentElementList elementList = doc.ContentElements;
            if (elementList.IsEmpty())
            {
                throw new System.Exception("get_IContentElements of " + doc.Name + " returned an empty list");
            }
            IEnumerator elemIter = elementList.GetEnumerator();
            Console.WriteLine("content element count: " + elementList.Count);
            while (elemIter.MoveNext())
            {
                IContentElement element = (IContentElement)elemIter.Current;
                if (element is IContentTransfer)
                {
                    IContentTransfer ct = (IContentTransfer)element;
                    System.Int32 sequenceNum = (int)element.ElementSequenceNumber;
                    System.IO.Stream ctStream = ct.AccessContentStream();
                    DirectoryInfo info = new DirectoryInfo(ceDownloadFolder);
                    if (!info.Exists)
                    {
                        info.Create();
                    }
                    string path = Path.Combine(ceDownloadFolder, ct.RetrievalName);
                    Console.WriteLine("Write content element " + sequenceNum + " to a file: " + path);
                    using (FileStream outputFileStream = new FileStream(path, FileMode.Create))
                    {
                        ctStream.CopyTo(outputFileStream);
                    }
                }
            }
            Console.WriteLine("Content Elements downloaded successfully");
        }
    }
}
