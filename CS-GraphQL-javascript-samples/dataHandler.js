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

// ***********************Data manipulation************************
function createDocResponse(response, div) {
  div.innerHTML +=
    "<br><strong>This operation will create 3 documents of different types- </strong><p>1. Document class</p><p>2. LoanApplicationDocument class</p><p>3. Lender class</p>";

  div.innerHTML += "<br><strong>Creating default Document</strong><br>";

  if (
    response.data !== undefined &&
    response.data !== null &&
    response.data.createDocument !== undefined &&
    response.data.createDocument !== null
  ) {
    let document = response.data.createDocument;

    div.innerHTML += JSON.stringify(document, null, 4);
    div.innerHTML += "<br><strong>...Done</strong>";
  } else {
    let defaultErr = `Unable to create document`;

    result = { 
        ok: false,
        errorMessage: (response.errors==null ? defaultErr :response.errors) };
    div.innerHTML += JSON.stringify(result, null, 4);
  }
}

function deleteDocResponse(response, div) {
  div.innerHTML +=
    "<br><strong>This operation will delete specified document </strong>";

  div.innerHTML += "<br><strong>Deleting Document</strong><br>";
  if (
    response.data !== undefined &&
    response.data !== null &&
    response.data.deleteDocument !== undefined &&
    response.data.deleteDocument !== null
  ) {
    let document = response.data;

    div.innerHTML += JSON.stringify(document, null, 4);
    div.innerHTML += "<br><strong>...Done</strong>";
  } else {
    let defaultErr = `Unable to delete document`;

    result = { 
        ok: false,
        errorMessage: (response.errors==null ? defaultErr :response.errors) };
    div.innerHTML += JSON.stringify(result, null, 4);
  }
}

function createDocContentResponse(response, div) {
  div.innerHTML +=
    "<br><strong>This operation will create a document containing content </strong>";

  div.innerHTML +=
    "<br><strong>Creating Document Containing Content</strong><br>";
  if (
    response.data !== undefined &&
    response.data !== null &&
    response.data.createDocument !== undefined &&
    response.data.createDocument !== null
  ) {
    let document = response.data;

    div.innerHTML += JSON.stringify(document, null, 4);
    div.innerHTML += "<br><strong>...Done</strong>";
  } else {
    let defaultErr = `Unable to create document`;

    result = { 
        ok: false,
        errorMessage: (response.errors==null ? defaultErr :response.errors) };
    div.innerHTML += JSON.stringify(result, null, 4);
  }
}

function downloadDocResponse(response, div) {
  if (response != null) {
    let ce = JSON.stringify(response, null, 4);

    if (ce === undefined || ce === null) {
      // Document with no content
      result = { ok: false, errorMessage: "Document has no content." };
      div.innerHTML += JSON.stringify(result, null, 4);
    } else {
      div.innerHTML += ce;
      div.innerHTML += "<br><strong>...Done</strong>";
    }
  } else {
    let defaultErr = `Unable to download document`;
    console.log(defaultErr);

    result = { 
        ok: false,
        errorMessage: (response.errors==null ? defaultErr :response.errors) };
    div.innerHTML += JSON.stringify(result, null, 4);
  }
}

function searchDocResponse(response, div) {
  if (response.data.documents != null) {
    let documents = response.data.documents;

    let docs = documents.documents;
    if (docs === undefined || docs === null) {
      result = { ok: false, errorMessage: "Document not found." };
      div.innerHTML += JSON.stringify(result, null, 4);
    } else {
      div.innerHTML += JSON.stringify(docs, null, 4);
      div.innerHTML += "<br><strong>...Done</strong>";
    }
  } else {
    let defaultErr = `Unable to search document`;

    result = { 
        ok: false,
        errorMessage: (response.errors==null ? defaultErr :response.errors) };
    div.innerHTML += JSON.stringify(result, null, 4);
  }
}

function searchFolderContaineesResponse(response, div) {
  if (response.data.folder != null) {
    let folder = response.data.folder;

    let ce = folder.containees.referentialContainmentRelationships;
    if (ce === undefined || ce === null) {
      // Document with no content
      result = { ok: false, errorMessage: "Folder has no content." };
      div.innerHTML += JSON.stringify(result, null, 4);
    } else {
      div.innerHTML += JSON.stringify(ce, null, 4);
      div.innerHTML += "<br><strong>...Done</strong>";
    }
  } else {
    let defaultErr = `Unable to find folder`;
    console.log(defaultErr);

    result = { 
      ok: false,
      errorMessage: (response.errors[0]==null ? defaultErr :response.errors) 
    };
    div.innerHTML += JSON.stringify(result, null, 4);
  }
}

function checkoutDocResponse(response, div) {
  if (response.data.checkoutDocument != null) {
    let checkoutDocument = response.data.checkoutDocument;

    let cr = checkoutDocument.reservation;
    let cv = checkoutDocument.currentVersion;

    if (cr === undefined || cr === null || cv === undefined || cv === null) {
      // Document with no content
      result = { ok: false, errorMessage: "Folder has no content." };
      div.innerHTML += JSON.stringify(result, null, 4);
    } else {
      div.innerHTML += JSON.stringify(checkoutDocument, null, 4);
      div.innerHTML += "<br><strong>...Done</strong>";
    }
  } else {
    let defaultErr = `Unable to checkin minor document`;
    console.log(defaultErr);

    result = { 
      ok: false,
      errorMessage: (response.errors[0]==null ? defaultErr :response.errors) 
    };
    div.innerHTML += JSON.stringify(result, null, 4);
  }
}

function checkinDocResponse(response, div) {
  if (response.data.checkinDocument != null) {
    let checkinDocument = response.data.checkinDocument;

    let cr = checkinDocument.currentVersion;

    if (cr === undefined || cr === null) {
      // Document with no content
      result = { ok: false, errorMessage: "Folder has no content." };
      div.innerHTML += JSON.stringify(result, null, 4);
    } else {
      div.innerHTML += JSON.stringify(checkinDocument, null, 4);
      div.innerHTML += "<br><strong>...Done</strong>";
    }
  } else {
    let defaultErr = `Unable to checkin minor document`;
    console.log(defaultErr);

    result = { 
      ok: false,
      errorMessage: (response.errors[0]==null ? defaultErr :response.errors) 
    };
    div.innerHTML += JSON.stringify(result, null, 4);
  }
}

function createFolderResponse(response, div) {
  if (response.data.topfolder != null || response.data.childfolder != null) {
    let topfolder = response.data.topfolder;
    let childfolder = response.data.childfolder;

    if (topfolder === undefined || topfolder === null) {
      // Document with no content
      result = { ok: false, errorMessage: "Folder has no content." };
      div.innerHTML += JSON.stringify(result, null, 4);
    } else {
      div.innerHTML += JSON.stringify(response.data, null, 4);
      div.innerHTML += "<br><strong>...Done</strong>";
    }
  } else {
    let defaultErr = `Unable to find folder`;
    console.log(defaultErr);

    result = { 
        ok: false,
        errorMessage: (response.errors[0]==null ? defaultErr :response.errors) };
    div.innerHTML += JSON.stringify(result, null, 4);
  }
}

function cancelCheckoutResponse(response, div) {
  if (response.data.cancelDocumentCheckout != null) {
    let cancelDocumentCheckout = response.data.cancelDocumentCheckout;

    if (
      cancelDocumentCheckout === undefined ||
      cancelDocumentCheckout === null
    ) {
      // Document with no content
      result = { ok: false, errorMessage: "Folder has no content." };
      div.innerHTML += JSON.stringify(result, null, 4);
    } else {
      div.innerHTML += JSON.stringify(cancelDocumentCheckout, null, 4);
      div.innerHTML += "<br><strong>...Done</strong>";
    }
  } else {
    result = { 
        ok: false,
        errorMessage: (response.errors==null ? defaultErr :response.errors) };
    div.innerHTML += JSON.stringify(result, null, 4);
  }
}

function retrieveDocResponse(response) {
  var selectedVal = document.getElementById("doc_operation").value;

  if (response.data.document != null) {
    let document = response.data.document;
    let cv = document.currentVersion;
    update_dom = true;
    currentVersion_id = cv.id;
    reservation_id = cv.reservation ? cv.reservation.id : "";

    if (selectedVal == "checkout_doc") {
      postRequest(checkOutDocumentGraphQL(currentVersion_id));
    } else if (selectedVal == "cancel_checkout") {
      postRequest(cancelCheckoutGraphQL());
    }
  }
}

function classDescResponse(response, div) {
  if (response.data.classDescription != null) {
    let classDesc = response.data.classDescription;

    let cd = classDesc.propertyDescriptions;

    if (cd.length == 0) {
      div.innerHTML = "No content.";
    } else {
      for (x in cd) {
        div.innerHTML += "<strong>" + x + ":";

        for (y in cd[x]) {
          div.innerHTML += "<br>" + y + ":" + cd[x][y] + "<br>";
        }
        div.innerHTML += "<br>";
      }

      if (classDesc.hasProperSubclassProperties) {
        let pd = classDesc.properSubclassPropertyDescriptions;

        if (pd.length == 0) {
          div.innerHTML += "No Property Descriptions.";
        } else {
          div.innerHTML += JSON.stringify(pd, null, 4);
          div.innerHTML += "<br><strong>...Done</strong>";
        }
      }
    }
  } else {
        result = { 
            ok: false,
            errorMessage: (response.errors==null ? defaultErr :response.errors) };
        div.innerHTML += JSON.stringify(result, null, 4); 
  }
}

function subClassDescResponse(response, div) {
  if (response.data.subClassDescriptions != null) {
    let subClassDescriptions = response.data.subClassDescriptions;

    let cd = subClassDescriptions.classDescriptions;

    if (cd.length == 0) {
      div.innerHTML = "No content.";
    } else {
      div.innerHTML += JSON.stringify(cd, null, 4);
      div.innerHTML += "<br><strong>...Done</strong>";
    }
  } else {
    result = { 
        ok: false,
        errorMessage: (response.errors==null ? defaultErr :response.errors) };
    div.innerHTML += JSON.stringify(result, null, 4);
  }
}

function domainAndOSResponse(response, div) {
  if (response.data.domain != null) {
    let domain = response.data.domain;

    let cd = domain.objectStores.objectStores;

    if (cd.length == 0) {
      div.innerHTML = "No content.";
    } else {
      div.innerHTML += JSON.stringify(domain, null, 4);
      div.innerHTML += "<br><strong>...Done</strong>";
    }
  } else {
    result = { 
        ok: false,
        errorMessage: (response.errors==null ? defaultErr :response.errors) };
    div.innerHTML += JSON.stringify(result, null, 4);
  }
}

function getTotalCountofObjectSearchGraphQLResponse(response, div) {
  console.log(JSON.stringify(response));
  if (response.data.documents != null) {
    let documents = response.data.documents;

    let pageInfo = documents.pageInfo;

    if (pageInfo.length == 0) {
      div.innerHTML = "No content.";
    } else {
      div.innerHTML +=
        "Total Count Of Object Search is" + ":" + pageInfo.totalCount + "<br>";
    }
  } else {
    result = { 
        ok: false,
        errorMessage: (response.errors==null ? defaultErr :response.errors) };
    div.innerHTML += JSON.stringify(result, null, 4);
  }
}

function updatePermissionsResponse(response, div) {
  if (
    response.data.updateDocument !== undefined &&
    response.data.updateDocument !== null
  ) {
    let document = response.data.updateDocument;
    div.innerHTML += JSON.stringify(document, null, 4);
    div.innerHTML += "<br><strong>...Done</strong>";
  } else {
    result = { 
        ok: false,
        errorMessage: (response.errors==null ? defaultErr :response.errors) };
    div.innerHTML += JSON.stringify(result, null, 4);
  }
}

function multipleRepositoryForObjectSearchesGraphQLResponse(response, div) {
  if (response.data.repositoryObjectSearches != null) {
    let repositoryObjectSearches = response.data.repositoryObjectSearches;

    let independentObjects = repositoryObjectSearches.independentObjects;

    // let pageInfo = repositoryObjectSearches.pageInfo;

    if (independentObjects.length == 0) {
      div.innerHTML = "No content.";
    } else {
      div.innerHTML += JSON.stringify(independentObjects, null, 4);
      div.innerHTML += "<br><strong>...Done</strong>";
    }
  } else {
    result = { 
        ok: false,
        errorMessage: (response.errors==null ? defaultErr :response.errors) };
    div.innerHTML += JSON.stringify(result, null, 4);
  }
}

function updateCustomSingleValueResponse(response, div) {
  if (
    response.data.updateDocument !== undefined &&
    response.data.updateDocument !== null
  ) {
    let document = response.data.updateDocument;
    div.innerHTML += JSON.stringify(document, null, 4);
    div.innerHTML += "<br><strong>...Done</strong>";
  } else {
    result = { 
        ok: false,
        errorMessage: (response.errors==null ? defaultErr :response.errors) };
    div.innerHTML += JSON.stringify(result, null, 4);
  }
}

function genericMutationsWithDependentObjectsResponse(response, div) {
  if (response.data.changeObject !== undefined && response.data.changeObject !== null) {
    let document = response.data.changeObject;
    div.innerHTML += JSON.stringify(document, null, 4);
    div.innerHTML += "<br><strong>...Done</strong>";
  } else {
    result = { 
        ok: false,
        errorMessage: (response.errors==null ? defaultErr :response.errors) };
    div.innerHTML += JSON.stringify(result, null, 4);
  }
}

function searchWithJoinGraphQLResponse(response, div) {
  if (
    response.data !== undefined &&
    response.data !== null &&
    response.data.documents != undefined &&
    response.data.documents != null
  ) {
    let docs = response.data.documents.documents;
    div.innerHTML += JSON.stringify(docs, null, 4);
    div.innerHTML += "<br><strong>...Done</strong>";
  } else {
    let defaultErr = `Unable to search document`;
    result = { 
        ok: false,
        errorMessage: (response.errors==null ? defaultErr :response.errors) };
    div.innerHTML += JSON.stringify(result, null, 4);
  }
}

function createLoanApplicationDocumentResponse(response, div) {
  div.innerHTML += "<br><strong>Creating LoanApplicationDocument</strong><br>";
  if (
    response.data !== undefined &&
    response.data !== null &&
    response.data.createDocument !== undefined &&
    response.data.createDocument !== null
  ) {
    let document = response.data.createDocument;

    div.innerHTML += JSON.stringify(document, null, 4);
    div.innerHTML += "<br><strong>...Done</strong>";
  } else {
    let defaultErr = `Unable to create document`;
    result = { 
        ok: false,
        errorMessage: (response.errors==null ? defaultErr :response.errors) };
    div.innerHTML += JSON.stringify(result, null, 4);
  }
}

function createLenderDocumentResponse(response, div) {
  div.innerHTML += "<br><strong>Creating Lender Document</strong><br>";
  if (
    response.data !== undefined &&
    response.data !== null &&
    response.data.createDocument !== undefined &&
    response.data.createDocument !== null
  ) {
    let document = response.data.createDocument;
    div.innerHTML += JSON.stringify(document, null, 4);
    div.innerHTML += "<br><strong>...Done</strong>";
  } else {
    let defaultErr = `Unable to create document`;
    result = { 
        ok: false,
        errorMessage: (response.errors==null ? defaultErr :response.errors) };
    div.innerHTML += JSON.stringify(result, null, 4);
  }
}

function createPingResponse(response, div) {
  div.innerHTML += "<br><strong>Ping Page's Response</strong><br>";
  if (response !== undefined && response !== null) {
    div.innerHTML += JSON.stringify(response, null, 4);
    div.innerHTML += "<br><strong>...Done</strong>";
  } else {
    let defaultErr = `Unable to connect to ping page`;
    result = { 
        ok: false,
        errorMessage: (response.errors==null ? defaultErr :response.errors) };
    div.innerHTML += JSON.stringify(result, null, 4);
  }
}

function createApiInfo(response, div) {
  div.innerHTML += "<br><strong>Fetch API Info </strong><br>";
  // console.log(response)
  if (response.data !== undefined && response.data !== null) {
    div.innerHTML += JSON.stringify(response.data._apiInfo, null, 4);
    div.innerHTML += "<br><strong>...Done</strong>";
  } else {
    let defaultErr = `Unable to fetch API`;
    result = { 
        ok: false,
        errorMessage: (response.errors==null ? defaultErr :response.errors) };
    div.innerHTML += JSON.stringify(result, null, 4);
  }
}
