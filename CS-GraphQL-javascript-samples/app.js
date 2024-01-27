/*
  Licensed Materials - Property of IBM (c) Copyright IBM Corp. 2019,2024 All Rights Reserved.

  US Government Users Restricted Rights - Use, duplication or disclosure restricted by GSA ADP Schedule Contract with
  IBM Corp.

  DISCLAIMER OF WARRANTIES :

  Permission is granted to copy and modify this Sample code, and to distribute modified versions provided that both the
  copyright notice, and this permission notice and warranty disclaimer appear in all copies and modified versions.

  THIS SAMPLE CODE IS LICENSED TO YOU AS-IS. IBM AND ITS SUPPLIERS AND LICENSORS DISCLAIM ALL WARRANTIES, EITHER
  EXPRESS OR IMPLIED, IN SUCH SAMPLE CODE, INCLUDING THE WARRANTY OF NON-INFRINGEMENT AND THE IMPLIED WARRANTIES OF
  MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE. IN NO EVENT WILL IBM OR ITS LICENSORS OR SUPPLIERS BE LIABLE FOR
  ANY DAMAGES ARISING OUT OF THE USE OF OR INABILITY TO USE THE SAMPLE CODE, DISTRIBUTION OF THE SAMPLE CODE, OR
  COMBINATION OF THE SAMPLE CODE WITH ANY OTHER CODE. IN NO EVENT SHALL IBM OR ITS LICENSORS AND SUPPLIERS BE LIABLE
  FOR ANY LOST REVENUE, LOST PROFITS OR DATA, OR FOR DIRECT, INDIRECT, SPECIAL, CONSEQUENTIAL, INCIDENTAL OR PUNITIVE
  DAMAGES, HOWEVER CAUSED AND REGARDLESS OF THE THEORY OF LIABILITY, EVEN IF IBM OR ITS LICENSORS OR SUPPLIERS HAVE
  BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
*/

let update_dom = true;
let reservation_id, currentVersion_id;

//Handles hiding file upload
function dropdownHandler() {
  var selectedVal = document.getElementById("doc_operation").value;
  if (selectedVal == "upload_content_doc" || selectedVal == "upload_stream_content_doc") {
    file = document.getElementById("file");
    showField(file);
  } else {
    file = document.getElementById("file");
    hideField(file);
  }
}

function getAuthType() {
  var jwtAuth = document.getElementById("jwt_slider");
  var usernameField = document.getElementById("username");
  var passwordField = document.getElementById("password");
  var jwtField = document.getElementById("jwt_token");

  if (jwtAuth.checked == false) {
    showField(usernameField);
    showField(passwordField);
    hideField(jwtField);
  } else {
    hideField(usernameField);
    hideField(passwordField);
    showField(jwtField);
  }
}

function hideField(field) {
  field.style.display = "none";
  for (const label of field.labels) {
    label.style.display = "none";
  }
}
function showField(field) {
  field.style.display = "inline";
  for (const label of field.labels) {
    label.style.display = "inline";
  }
}

function disableButton(id){
  let button = document.getElementById(id)
  button.disabled = true;
  button.value = "Pending";
}

function enableButton(id){
  let button = document.getElementById(id)
  button.disabled = false;
  button.value = "Execute";
}

function getForm() {
  setGraphQLEndPoint(document.getElementById("endpoint").value);
  setXSRFToken(document.getElementById("xsrf_token").value);
  setObjectStore(document.getElementById("object_store_name").value);

  setFileId(document.getElementById("file_id").value);
  if (document.getElementById("jwt_slider").checked == true) {
    setJwtToken(document.getElementById("jwt_token").value);
  } else {
    setUserName(document.getElementById("username").value);
    setPassword(document.getElementById("password").value);
  }
}

function executeHandler() {
  getForm();
  disableButton("execute_button")
  document.getElementById("demo").innerHTML = "";
  var selectedVal = document.getElementById("doc_operation").value;

  switch (selectedVal) {
    case "ping":
      sendRequest("ping");
      break;
    case "create_doc":
      sendGraphRequest(createDocumentGraphQL(), "create_doc");
      //Synchronous XMLHttpRequest on the main thread is deprecated because of its detrimental effects to the end user's experience.
      //Thus adding interval
      setTimeout(() => {
        sendGraphRequest(
          createLoanApplicationDocumentGraphQL(),
          "create_LoanApplication"
        );
      }, 3000);
      setTimeout(() => {
        sendGraphRequest(createLenderDocumentGraphQL(), "create_Lender");
      }, 6000);
      break;
    case "create_content_doc":
      sendGraphRequest(createDocumentContentGraphQL(), "create_content_doc");
      break;
    case "upload_content_doc":
      sendGraphRequest(createDocumentContentGraphQL(), "upload_content_doc");
      break;
    case "upload_stream_content_doc":
      sendGraphRequest(
        createDocumentContentGraphQL(),
        "upload_stream_content_doc"
      );
      break;
    case "fetch_api":
      sendGraphRequest(fetchApiInfo(), "fetch_api");
      break;
    case "fetch_xsrf":
      sendGraphRequest("", "fetch_xsrf");
      break;
    case "delete_doc":
      sendGraphRequest(deleteDocumentGraphQL(), "delete_doc");
      break;
    case "download_doc":
      sendGraphRequest(downloadDocumentGraphQL(), "download_doc");
      break;
    case "checkinminor_doc":
      sendGraphRequest(checkInDocAsMinorVersionGraphQL());
      break;
    case "checkinmajor_doc":
      sendGraphRequest(checkInDocAsMajorVersionGraphQL());
      break;
    case "checkout_doc":
      sendGraphRequest(checkOutDocumentGraphQL());
      break;
    case "cancel_checkout":
      update_dom = false;
      sendGraphRequest(retrieveDocGraphQL());
      break;
    case "create_folder":
      sendGraphRequest(createFolderSubFolderGraphQL());
      break;
    case "search_doc":
      sendGraphRequest(searchDocumentsGraphQL());
      break;
    case "search_folder":
      sendGraphRequest(searchForFolderContaineesGraphQL());
      break;
    case "search_with_join":
      sendGraphRequest(searchWithJoinGraphQL());
      break;
    case "list_meta_cd":
      sendGraphRequest(listPropertyDescriptionsGraphQL());
      break;
    case "list_sub_cd":
      sendGraphRequest(listSubClassDescriptionsGraphQL());
      break;
    case "list_domain_os":
      sendGraphRequest(listdomainAndObjectStoresGraphQL());
      break;
    case "list_subClass_propDesc":
      sendGraphRequest(subClassPropDescGraphQL());
      break;
    case "get_total_count_of_ObjectSearch":
      sendGraphRequest(getTotalCountofObjectSearchGraphQL());
      break;
    case "update_permissions":
      sendGraphRequest(updatePermissionsGraphQL());
      break;
    case "multiple_repository_object_searches":
      sendGraphRequest(multipleRepositoryForObjectSearchesGraphQL());
      break;
    case "updating_custom_single_value":
      sendGraphRequest(updateCustomSingleValueGraphQL());
      break;
    case "generic_mutations_with_dependent_objects":
      sendGraphRequest(genericMutationsWithDependentObjectsGraphQL());
      break;
    default:
      document.getElementById("demo").innerHTML = "Select an Operation";
  }
}



// HTTP call for graphQL API
function sendGraphRequest(data, query_op) {
  var postUrl, base64, xhttp, response, div, jwtAuth;
  xhttp = new XMLHttpRequest();
  xhttp.withCredentials = true;
  jwtAuth = document.getElementById("jwt_slider").checked;
  postUrl = appConfig.graphql + "/graphql";
  xhttp.open("POST", postUrl, true);
  if (jwtAuth == false) {
    base64 = window.btoa(appConfig.username + ":" + appConfig.password);
    xhttp.setRequestHeader("Authorization", "Basic " + base64);
  } else {
    xhttp.setRequestHeader("Authorization", "Bearer " + appConfig.jwtToken);
  }
  xhttp.setRequestHeader("ECM-CS-XSRF-Token", appConfig.xsrfToken);
  xhttp.setRequestHeader("Access-Control-Allow-Origin", "*");
  div = document.getElementById("demo"); //DOM element: for showing response on UI
  switch (query_op) {
    case "download_doc":
      xhttp.setRequestHeader("Content-Type", "application/graphql");
      xhttp.onreadystatechange = function () {
        if (this.readyState == 4) {
          if (this.status == 200) {
            response = JSON.parse(this.responseText);
            if (update_dom == true) {
              dataHandler(response, div, query_op);
              try {
                download_data = {
                  url: response.data.document.contentElements[0].downloadUrl,
                  filename:
                    response.data.document.contentElements[0].retrievalName,
                };
                div.innerHTML +=
                  "<br> Download URL: " + appConfig.graphql + download_data.url;
                div.innerHTML +=
                  "<br> Download filename: " + download_data.filename;
                sendRequest("download", download_data);
              } catch (error) {
                enableButton("execute_button")
                div.innerHTML += "<br> Invalid download URL";
              }
            } else {
              retrieveDocResponse(response);
            }
          } else {
            enableButton("execute_button")
            div.innerHTML =
              "Unsuccessful request, check console for potential solution";
          }
        }
      };
      xhttp.send(data);
      break;
    case "create_content_doc":
      xhttp.setRequestHeader("Content-Type", "application/graphql");
      xhttp.onreadystatechange = function () {
        if (this.readyState == 4) {
          if (this.status == 200) {
            response = JSON.parse(this.responseText);
            if (update_dom == true) {
              dataHandler(response, div, query_op);
            } else {
              retrieveDocResponse(response);
            }
          } else {
            div.innerHTML =
              "Unsuccessful request, check console for potential solution";
          }
          enableButton("execute_button")
        }
      };
      // console.log(response)
      xhttp.send(data);
      break;
    case "upload_stream_content_doc":
      xhttp.setRequestHeader("ECM-CS-Use-Multipart-Streaming", "true"); 
    case "upload_content_doc":
      try {
        var fileSample = document.getElementById("file").files[0];
      } catch {
        div.innerHTML = "File uploaded is invalid, try again";
        return;
      }
      var operation = {
        query: data,
        variables: { nFile: null },
      };
      var map = {
        nFile: ["variables.file"],
      };
      //create form data
      formData = new FormData();
      formData.append("operations", JSON.stringify(operation));
      formData.append("map", JSON.stringify(map));
      formData.append("nFile", fileSample);

      xhttp.onreadystatechange = function () {
        if (this.readyState == 4) {
          if (this.status == 200) {
            response = JSON.parse(this.responseText);
            if (update_dom == true) {
              dataHandler(response, div, query_op);
            } else {
              retrieveDocResponse(response);
            }
          } else {
            div.innerHTML =
              "Unsuccessful request, check console for potential solution";
          }
          enableButton("execute_button")        
        }
      };
      xhttp.send(formData);
      break;
    default:
      xhttp.setRequestHeader("Content-Type", "application/graphql");
      xhttp.onreadystatechange = function () {
        if (this.readyState == 4) {
          if (this.status == 200) {
            response = JSON.parse(this.responseText);
            if (update_dom == true) {
              dataHandler(response, div, query_op);
            } else {
              retrieveDocResponse(response);
            }
          } else {
            div.innerHTML =
              "Unsuccessful request, check console for potential solution";
          }
          enableButton("execute_button")
        }
      };
      // console.log(response)
      xhttp.send(data);
      break;
  }
}

function sendRequest(operation, data) {
  var getUrl, base64, xhttp, response, div, jwtAuth;
  xhttp = new XMLHttpRequest();
  xhttp.withCredentials = true;
  jwtAuth = document.getElementById("jwt_slider").checked;
  div = document.getElementById("demo"); //DOM element: for showing response on UI
  switch (operation) {
    case "ping":
      getUrl = appConfig.graphql + "/ping";
      xhttp.open("GET", getUrl, true);
      xhttp.setRequestHeader("Access-Control-Allow-Origin", "*");
      xhttp.onreadystatechange = function () {
        if (this.readyState == 4) {
          if (this.status == 200) {
            // Response
            xsrfToken = this.getResponseHeader("ECM-CS-XSRF-Token");
            document.getElementById("xsrf_token").value = xsrfToken;
            response = JSON.parse(this.responseText);
            response["XSRF_Token"] = xsrfToken;
            dataHandler(response, div, operation);
          } else {
            div.innerHTML =
              "Unsuccessful request, check console for potential solution";
          }
          enableButton("execute_button")
        }
      };
      xhttp.send();
      break;
    case "download":
      getUrl = appConfig.graphql + data.url;
      xhttp.open("GET", getUrl, true);
      if (jwtAuth == false) {
        base64 = window.btoa(appConfig.username + ":" + appConfig.password);
        xhttp.setRequestHeader("Authorization", "Basic " + base64);
      } else {
        xhttp.setRequestHeader("Authorization", "Bearer " + appConfig.jwtToken);
      }
      xhttp.setRequestHeader("ECM-CS-XSRF-Token", appConfig.xsrfToken);
      xhttp.setRequestHeader("Access-Control-Allow-Origin", "*");
      xhttp.setRequestHeader(
        "Accept",
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange"
      );
      xhttp.setRequestHeader("Range", "bytes=1024000");
      xhttp.responseType = "blob";
      xhttp.onreadystatechange = function () {
        if (this.readyState == 4) {
          if (this.status == 200) {
            const blob = this.response;
            contentDisposition = this.getResponseHeader("Content-Disposition");
            if (contentDisposition) {
              const downloadLink = document.createElement("a");
              downloadLink.href = URL.createObjectURL(blob);
              downloadLink.download = data.filename;
              document.body.appendChild(downloadLink);
              downloadLink.click();
              document.body.removeChild(downloadLink);
            }
          } else {
            div.innerHTML =
              "Unsuccessful request, check console for potential solution";
          }
          enableButton("execute_button")
        }
      };
      xhttp.send(data);
      break;
  }
}


// Handling/ manipulation API response
function dataHandler(response, div, query_op) {
  var selectedVal = document.getElementById("doc_operation").value;

  switch (selectedVal) {
    case "ping":
      createPingResponse(response, div);
      break;
    case "create_doc":
      if (query_op == "create_doc") {
        createDocResponse(response, div);
      }
      if (query_op == "create_LoanApplication") {
        createLoanApplicationDocumentResponse(response, div);
      }
      if (query_op == "create_Lender") {
        createLenderDocumentResponse(response, div);
      }
      break;
    case "upload_stream_content_doc":
    case "upload_content_doc":
      createDocContentResponse(response, div);
      break;
    case "create_content_doc":
      createDocContentResponse(response, div);
      break;
    case "fetch_api":
      createApiInfo(response, div);
      break;
    case "delete_doc":
      deleteDocResponse(response, div);
      break;
    case "download_doc":
      downloadDocResponse(response, div);
      break;
    case "checkout_doc":
      retrieveDocResponse(response);
      checkoutDocResponse(response, div);
      break;
    case "cancel_checkout":
      cancelCheckoutResponse(response, div);
      break;
    case "checkinminor_doc":
      checkinDocResponse(response, div);
      break;
    case "checkinmajor_doc":
      checkinDocResponse(response, div);
      break;
    case "create_folder":
      createFolderResponse(response, div);
      break;
    case "search_doc":
      searchDocResponse(response, div);
      break;
    case "search_folder":
      searchFolderContaineesResponse(response, div);
      break;
    case "search_with_join":
      searchWithJoinGraphQLResponse(response, div);
      break;
    case "list_meta_cd":
      classDescResponse(response, div);
      break;
    case "list_subClass_propDesc":
      classDescResponse(response, div);
      break;
    case "list_sub_cd":
      subClassDescResponse(response, div);
      break;
    case "list_domain_os":
      domainAndOSResponse(response, div);
      break;
    case "get_total_count_of_ObjectSearch":
      getTotalCountofObjectSearchGraphQLResponse(response, div);
      break;
    case "update_permissions":
      updatePermissionsResponse(response, div);
      break;
    case "multiple_repository_object_searches":
      multipleRepositoryForObjectSearchesGraphQLResponse(response, div);
      break;
    case "updating_custom_single_value":
      updateCustomSingleValueResponse(response, div);
      break;
    case "generic_mutations_with_dependent_objects":
      genericMutationsWithDependentObjectsResponse(response, div);
      break;
    default:
      document.getElementById("demo").innerHTML = "";
      break;
  }
}
