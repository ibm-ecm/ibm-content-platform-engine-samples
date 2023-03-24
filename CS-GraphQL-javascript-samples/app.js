/*
  Licensed Materials - Property of IBM (c) Copyright IBM Corp. 2019,2023 All Rights Reserved.

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

function dropdownHandler() {
  document.getElementById("demo").innerHTML = "";
  // console.log(document.getElementById("demo"))
  var selectedVal = document.getElementById("doc_operation").value;

  switch (selectedVal) {
    case "ping":
      postRequest("", "ping");
      break;
    case "create_doc":
      postRequest(createDocumentGraphQL(), "create_doc");
      //Synchronous XMLHttpRequest on the main thread is deprecated because of its detrimental effects to the end user's experience.
      //Thus adding interval
      setTimeout(() => {
        postRequest(
          createLoanApplicationDocumentGraphQL(),
          "create_LoanApplication"
        );
      }, 3000);
      setTimeout(() => {
        postRequest(createLenderDocumentGraphQL(), "create_Lender");
      }, 6000);
      break;
    case "create_content_doc":
      postRequest(createDocumentContentGraphQL(), "create_content_doc");
      break;
    case "fetch_api":
      postRequest(fetchApiInfo(), "fetch_api");
      break;
    case "fetch_xsrf":
      postRequest("", "fetch_xsrf");
      break;
    case "delete_doc":
      postRequest(deleteDocumentGraphQL(), "delete_doc");
      break;
    case "download_doc":
      postRequest(downloadDocumentGraphQL());
      break;
    case "checkinminor_doc":
      postRequest(checkInDocAsMinorVersionGraphQL());
      break;
    case "checkinmajor_doc":
      postRequest(checkInDocAsMajorVersionGraphQL());
      break;
    case "checkout_doc":
      postRequest(checkOutDocumentGraphQL());
      break;
    case "cancel_checkout":
      update_dom = false;
      postRequest(retrieveDocGraphQL());
      break;
    case "create_folder":
      postRequest(createFolderSubFolderGraphQL());
      break;
    case "add_doc":
      postRequest(downloadDocumentGraphQL());
      break;
    case "search_doc":
      postRequest(searchDocumentsGraphQL());
      break;
    case "search_folder":
      postRequest(searchForFolderContaineesGraphQL());
      break;
    case "search_with_join":
      postRequest(searchWithJoinGraphQL());
      break;
    case "list_meta_cd":
      postRequest(listPropertyDescriptionsGraphQL());
      break;
    case "list_sub_cd":
      postRequest(listSubClassDescriptionsGraphQL());
      break;
    case "list_domain_os":
      postRequest(listdomainAndObjectStoresGraphQL());
      break;
    case "list_subClass_propDesc":
      postRequest(subClassPropDescGraphQL());
      break;
    case "get_total_count_of_ObjectSearch":
      postRequest(getTotalCountofObjectSearchGraphQL());
      break;
    case "update_permissions":
      postRequest(updatePermissionsGraphQL());
      break;
    case "multiple_repository_object_searches":
      postRequest(multipleRepositoryForObjectSearchesGraphQL());
      break;
    case "updating_custom_single_value":
      postRequest(updateCustomSingleValueGraphQL());
      break;
    case "generic_mutations_with_dependent_objects":
      postRequest(genericMutationsWithDependentObjectsGraphQL());
      break;
    default:
      document.getElementById("demo").innerHTML = "Select an Operation";
  }
}

function getForm() {
  // console.log("test")
  appConfig.os = document.getElementById("object_store_name").value;
  appConfig.graphql = document.getElementById("endpoint").value;
  appConfig.username = document.getElementById("username").value;
  appConfig.password = document.getElementById("password").value;
  appConfig.fileId = document.getElementById("file_id").value;
  appConfig.xsrfToken = document.getElementById("xsrf_token").value;
  if (appConfig.debug == "true") {
    appConfig.os = "";
    appConfig.graphql =
      "";
    appConfig.username = "";
    appConfig.password = "";
  }

  dropdownHandler();
}

// HTTP call for graphQL API
function postRequest(data, query_op) {
  var getUrl, postUrl, base64, xhttp, response, div;
  xhttp = new XMLHttpRequest();
  xhttp.withCredentials = true;

  switch (query_op) {
    case "ping":
      getUrl = appConfig.graphql + "/ping";
      div = document.getElementById("demo"); //DOM element: for showing response on UI
      xhttp.open("GET", getUrl, true);
      xhttp.onreadystatechange = function () {
        if (this.readyState == 4){
          if (this.status == 200) {
            // Response
            xsrfToken = this.getResponseHeader("ECM-CS-XSRF-Token");
            document.getElementById("xsrf_token").value = xsrfToken;
            response = JSON.parse(this.responseText);
            response["XSRF_Token"]=xsrfToken;
            dataHandler(response, div, query_op);
          } else {
            div.innerHTML = "Unsuccessful request, check console for potential solution";
          }
        }
      };
      xhttp.send();
      break;
    case "create_content_doc":
      fileURL = document.URL + "sample.xml";
      getFile(fileURL).then(function (fileResponse) {
        var blob = new Blob([fileResponse], { type: "text/xml" });
        var fileSample = new File([blob], "sample.xml", { type: "text/xml" });
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
        formData.append("nFile", fileSample, "sample.xml");

        postUrl = appConfig.graphql + "/graphql";
        base64 = window.btoa(appConfig.username + ":" + appConfig.password);
        xhttp.open("POST", postUrl);
        xhttp.setRequestHeader("Authorization", "Basic " + base64);
        xhttp.setRequestHeader("ECM-CS-XSRF-Token", appConfig.xsrfToken);
        div = document.getElementById("demo"); //DOM element: for showing response on UI
        xhttp.onreadystatechange = function () {
          if (this.readyState == 4){
            if (this.status == 200) {
              response = JSON.parse(this.responseText);
              if (update_dom == true) {
                dataHandler(response, div, query_op);
              } else {
                retrieveDocResponse(response);
              }
            } else {
              div.innerHTML = "Unsuccessful request, check console for potential solution";
            }
          }
        };
        xhttp.send(formData);
      });
      break;

    default:
      postUrl = appConfig.graphql + "/graphql";
      base64 = window.btoa(appConfig.username + ":" + appConfig.password);
      xhttp.open("POST", postUrl, true);
      xhttp.setRequestHeader(
        "Content-Type", "application/x-www-form-urlencoded"
      );
      xhttp.setRequestHeader("Authorization", "Basic " + base64);
      xhttp.setRequestHeader("ECM-CS-XSRF-Token", appConfig.xsrfToken);
      div = document.getElementById("demo"); //DOM element: for showing response on UI
      xhttp.onreadystatechange = function () {
        if (this.readyState == 4){
          if (this.status == 200) {
            response = JSON.parse(this.responseText);
            if (update_dom == true) {
              dataHandler(response, div, query_op);
            } else {
              retrieveDocResponse(response);
            }
          } else {
            div.innerHTML = "Unsuccessful request, check console for potential solution";
          }
        }
      };
      // console.log(response)
      xhttp.send(JSON.stringify({ query: data }));
      break;
  }
}

function getFile(url) {
  return new Promise(function (resolve, reject) {
    var xhttp = new XMLHttpRequest();
    xhttp.onload = function () {
      if (xhttp.readyState == 4 && xhttp.status == 200) {
        resolve(xhttp.responseText);
        console.log("inside:" + xhttp.responseText);
      } else {
        reject({
          status: xhttp.status,
          statusText: xhttp.statusText,
        });
      }
    };
    xhttp.onerror = function () {
      reject({
        status: xhttp.status,
        statusText: xhttp.statusText,
      });
    };
    xhttp.open("GET", url);
    xhttp.send();
  });
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
    case "add_doc":
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
