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

// Create document with content
function createDocumentGraphQL() {
  return `
mutation {
    createDocument(
        repositoryIdentifier:"${appConfig.os}"
        fileInFolderIdentifier:"/Test"
        documentProperties: {
            name: "Test Doc" 
            properties:[
            ]
        }
        checkinAction: {}
    ) 
    { 
        id 
        name 
    } 
}`;
}

function deleteDocumentGraphQL() {
  return `
mutation {
  deleteDocument(
    repositoryIdentifier:"${appConfig.os}"
    identifier:"${appConfig.fileId}"
  )
  {
    className
    id
  }
}`;
}

function createDocumentContentGraphQL() {
  return `
    mutation createDocument($nFile: String)
    {
      createDocument(
        repositoryIdentifier: "${appConfig.os}"
        fileInFolderIdentifier:"/Test"
        classIdentifier: "Document"
        checkinAction: {}
        documentProperties: {
          name: "test double byte"
          contentElements: {
            replace: [
              {
                type: CONTENT_TRANSFER
                subContentTransfer: {
                  content: $nFile
                }
              }
            ]
          }
        }
      )
      {
        className
        id
        name
      }
    }
    `;
}

function fetchApiInfo() {
  return `{
	_apiInfo(repositoryIdentifier:"${appConfig.os}")
  {
    buildDate
    implementationVersion
    buildNumber
    productVersion
    implementationTitle
    cpeInfo {
      cpeURL
      cpeUser
      repositoryName
    }
  }
}`;
}

// Download document with content
function downloadDocumentGraphQL() {
  return `
    {
        document(
          repositoryIdentifier:"${appConfig.os}"
          identifier:"${appConfig.fileId}"
        )
        {
          className
          id
          name
          majorVersionNumber
          minorVersionNumber
          contentElements {
                          contentType,
                          elementSequenceNumber,
                          ... on ContentTransfer {
                              contentSize,
                              retrievalName,
                              downloadUrl
                          }
                      }
        }
      }    
    `;
}

// Check-out document
function checkOutDocumentGraphQL() {
  return `mutation {
        checkoutDocument(
    repositoryIdentifier:"${appConfig.os}",
            identifier:"${appConfig.fileId}",
          checkoutAction: {
            reservationProperties: 
              [
                    {DocumentTitle: "Doc with Content"}
              ]   
    })
      {
        id
        name
        reservation
        {
          id
          name
          dateCreated
        }
        currentVersion {
            id
            majorVersionNumber
            minorVersionNumber
            versionStatus
        }
      }
    }`;
}

// Check-in document as a minor version
function checkInDocAsMinorVersionGraphQL() {
  return `
    mutation{
        checkinDocument(
        repositoryIdentifier:"${appConfig.os}"
        identifier:"${appConfig.fileId}"
        checkinAction:{
            checkinMinorVersion:true
        }
        ) {
        id
        name
        reservation
        {
            id
            name
            dateCreated
        }
        currentState
        currentVersion {
            id
            majorVersionNumber
            minorVersionNumber
            versionStatus
        }
        versionStatus
    
        }
    }`;
}

// Check-in document as a major version
function checkInDocAsMajorVersionGraphQL() {
  return `
mutation{
    checkinDocument(
      repositoryIdentifier:"${appConfig.os}"
      identifier:"${appConfig.fileId}"
      checkinAction:{
        checkinMinorVersion:false
      }
    ) {
      id
      name
      reservation
      {
        id
        name
        dateCreated
      }
      currentState
      currentVersion {
        id
        majorVersionNumber
        minorVersionNumber
        versionStatus
      }
      versionStatus
  
    }
  }`;
}

// Create folder and sub-folders
function createFolderSubFolderGraphQL() {
  return `
mutation{
    topfolder: createFolder(
      repositoryIdentifier:"${appConfig.os}"
      folderProperties:{
        name:"Test"
        parent:{
          identifier:"/"
        }
      }
    )
    {name
    className
    pathName
    }
    childfolder: createFolder(
      repositoryIdentifier:"${appConfig.os}"
      folderProperties:{
        name:"Test subfolder1"
        parent:{
          identifier:"/Test"
        }
      }
    )
    {name
    className
    pathName
    }
  } `;
}

// Add/file documents into folder
function addDocumentToFolderGraphQL() {
  return `
    mutation {
        createDocument(
            repositoryIdentifier:"${appConfig.os}"
          fileInFolderIdentifier:"/Test"
            documentProperties: {
                name: "Doc1_with_content" 
                properties:[
                ]
            }
            checkinAction: {}
        ) 
        { 
            id 
            name 
          className
        } 
    } `;
}

// Search Documents
function searchDocumentsGraphQL() {
  return `
    {
        documents(
          repositoryIdentifier:"${appConfig.os}"
          from:"Document"
          where:"[DateCreated] > 20180815T070000Z AND [IsCurrentVersion] = True"
          orderBy:"DocumentTitle"
          pageSize:20
        ) {
          documents {
            dateCreated
            id
            name
            majorVersionNumber
            minorVersionNumber
            mimeType
          }
          pageInfo {
            token
          }
        }
      }`;
}

// Folder navigation/search for folder containees
function searchForFolderContaineesGraphQL() {
  return `
    query 
        { folder(
        repositoryIdentifier:"${appConfig.os}"
        identifier:"${appConfig.fileId}"
      )
      {
        className
        id
        name
        pathName
        containees{
          referentialContainmentRelationships {
            id
            name
          }
        }
      }
}    `;
}

function retrieveDocGraphQL() {
  return `
    query{
        document(identifier:"${appConfig.fileId}"
        repositoryIdentifier:"${appConfig.os}") {
          id
          currentVersion {
            id
            minorVersionNumber
            majorVersionNumber
            versionStatus
            isReserved
            reservation {
              id
            }
            
          }
          versionStatus
          currentState
          versionSeries {
            id
          }
        }
      }`;
}

// Cancel check-out document
function cancelCheckoutGraphQL() {
  return `
    mutation{
        cancelDocumentCheckout(identifier:"${currentVersion_id}"
        repositoryIdentifier:"${appConfig.os}") {
          id
        }
      }`;
}

// Retrieving metadata - classDescription
function listPropertyDescriptionsGraphQL() {
  return `
    { 
  classDescription(
    repositoryIdentifier:"${appConfig.os}"
    identifier:"ObjectStore") 
  {
   	id
    propertyDescriptions(filter: {isHidden:true, isSystemOwned:true})
    {
      name
      displayName
      symbolicName
      dataType
      isReadOnly
      isOrderable
      isSystemOwned
      isSelectable
      isSearchable
      cardinality
      settability   
    }    
   }
  }`;
}

// Retrieving subclasses of a certain class
function listSubClassDescriptionsGraphQL() {
  return `
    {
        subClassDescriptions(repositoryIdentifier: "${appConfig.os}"
            identifier: "Document",
            pageSize: 14)
        {
            classDescriptions {
                id
                name
                symbolicName
                displayName
                descriptiveText
                superClassDescription {
                      name
                }
          }
          pageInfo {
                token
                totalCount
          }
            
        }
    }
    `;
}

// Retrieving a domain and its object stores
function listdomainAndObjectStoresGraphQL() {
  return `{
        domain {
        id
        name
        objectStores {
            objectStores {
            id
            symbolicName
            displayName
            }
        }
    }  
}`;
}

// Retrieving a class description along with all its subclasses’ property descriptions
function subClassPropDescGraphQL() {
  return `
    {
        classDescription(
              repositoryIdentifier: "${appConfig.os}"
              identifier: "ObjectStore") 
        {
          name
          displayName
          symbolicName
          propertyDescriptions (
            filter: {
              isHidden: false 
            }) 
          {
            ...propDescFieldsFragment
          }
          hasProperSubclassProperties
          properSubclassPropertyDescriptions(
            filter: {
              isHidden: false
            }) 
          {
            ...propDescFieldsFragment
          }
        }
      }
      
      fragment propDescFieldsFragment on PropertyDescription {
        id
        symbolicName
        displayName
        descriptiveText
        dataType
        cardinality
        isReadOnly
        isValueRequired
        settability
        ... on PropertyDescriptionBoolean {
          propertyDefaultBoolean
        }
        ... on PropertyDescriptionString {
          propertyDefaultString
          maximumLengthString
        }
        ... on PropertyDescriptionInteger32 {
          propertyDefaultInteger32
          propertyMinimumInteger32
          propertyMaximumInteger32
        }
        ... on PropertyDescriptionId {
          propertyDefaultId
        }
        ... on PropertyDescriptionDateTime {
          propertyDefaultDateTime
          propertyMinimumDateTime
          propertyMaximumDateTime
        }
        ... on PropertyDescriptionFloat64 {
          propertyDefaultFloat64
          propertyMinimumFloat64
          propertyMaximumFloat64
        }
      }`;
}

// Get Total Count of an Object search
function getTotalCountofObjectSearchGraphQL() {
  return `
    {
      documents(
        repositoryIdentifier:"${appConfig.os}"
        from:"Document"
        where:"[DateCreated] > 20180815T070000Z AND [IsCurrentVersion] = True"
        orderBy:"DocumentTitle"
        options:"COUNT_LIMIT 5000"
        pageSize:20
      ) {
        documents {
          dateCreated
          id
          name
          majorVersionNumber
          minorVersionNumber
          mimeType
        }
        pageInfo {
          token
          totalCount
        }
      } 
  }`;
}

// Updates the permissions of a document
function updatePermissionsGraphQL() {
  return `mutation {
          updateDocument(
            repositoryIdentifier:"${appConfig.os}"
            identifier:"${appConfig.fileId}"
            documentProperties:{
              permissions:{
                replace:[
                  {
                    type:ACCESS_PERMISSION
                    inheritableDepth:OBJECT_ONLY
                    accessMask:998903
                    subAccessPermission:{
                      accessType:ALLOW
                      granteeName:"CEAdmin"
                    }
                  }
                ]
              }
            }
          )
          {
            id
            name
          }
        }`;
}

// function for Multiple repository for Object searches
function multipleRepositoryForObjectSearchesGraphQL() {
  return `
    {
      repositoryObjectSearches(
        repositoryIdentifier:"${appConfig.os}"
        searches:[
          {
            from:"Folder"
            where:"[DateCreated] > 20180815T070000Z"
            orderBy:"FolderName ASC"
          }
          {
            from:"Document"
            where:"[DateCreated] > 20180815T070000Z AND [IsCurrentVersion] = True"
            orderBy:"DocumentTitle ASC"
          }
        ]
        pageSize:15
      )
      {
        independentObjects {
          className 
          objectReference {
            identifier
          }
          ... on Folder {
              dateCreated
              id
              name
              pathName
          }
          ... on Document {
            dateCreated
            id
            name
            majorVersionNumber
            minorVersionNumber
            mimeType
          }
        }
        pageInfo {
          token
        }
      }
    }`;
}

// Updating custom single value object properties
function updateCustomSingleValueGraphQL() {
  return `mutation {
        updateDocument(
          repositoryIdentifier:"${appConfig.os}"
          identifier:"${appConfig.fileId}"
          documentProperties:{
            objectProperties: [
              {
                identifier:"StoragePolicy"
                objectReferenceValue:{
                  identifier:"{8752A722-6016-4F04-9A43-A0F3D006E1ED}"
                }
              }
            ]
          }
        )
        {
          id
          name
        }
      }
      `;
}

// Generic mutations with dependent objects
function genericMutationsWithDependentObjectsGraphQL() {
  return `mutation {
          changeObject(
            repositoryIdentifier:"${appConfig.os}"
            classIdentifier:"Document"
            identifier:"{A0D4E673-0000-CA1E-86CE-EDE44E71DFAE}"
            objectProperties:[
              {
                identifier:"Permissions"
                dependentObjectListValue:{
                  replace:[
                    {
                      classIdentifier:"AccessPermission"
                      properties:[
                        {InheritableDepth:0}
                        {GranteeName:"CEAdmin"}
                        {AccessType:1}
                        {AccessMask:998903}
                      ]
                    }
                    {
                      classIdentifier:"AccessPermission"
                      properties:[
                        {InheritableDepth:0}
                        {GranteeName:"intg_admin"}
                        {AccessType:1}
                        {AccessMask:998903}
                      ]
                    }
                    {
                      classIdentifier:"AccessPermission"
                      properties:[
                        {InheritableDepth:0}
                        {GranteeName:"CEAdminGroup"}
                        {AccessType:1}
                        {AccessMask:998903}
                      ]
                    }
                    {
                      classIdentifier:"AccessPermission"
                      properties:[
                        {InheritableDepth:0}
                        {GranteeName:"#AUTHENTICATED-USERS"}
                        {AccessType:1}
                        {AccessMask:131201}
                      ]
                    }
                    {
                      classIdentifier:"AccessPermission"
                      properties:[
                        {InheritableDepth:0}
                        {GranteeName:"pwtest100"}
                        {AccessType:1}
                        {AccessMask:131201}
                      ]
                    }
                  ]
                }
              }
            ]
          )
          {
            className
            ... on Document {
              id
              name
              versionStatus
              majorVersionNumber
              minorVersionNumber
            }
          }
        }
          `;
}

function searchWithJoinGraphQL() {
  return `
    query{
      documents(
        repositoryIdentifier:"${appConfig.os}"
        from:" Lender e INNER JOIN LoanApplicationDocument a ON a.LenderName = e.LenderName"
        where:" e.LenderName LIKE 'HD%'"
        orderBy:" a.LenderName DESC"
      ) {
        documents {
          id
          name
          properties(includes: ["LenderName","BorrowerName","LoanApplicationNumber"]) {
            id
            label
            type
            cardinality
            value
            ... on ObjectProperty {
              objectValue {
                className
                ... on CmAbstractPersistable {
                  creator
                  dateCreated
                  properties(includes: ["LenderName"]) {
                    id
                    label
                    type
                    cardinality
                    value
                  }
                }
              }
            }
          }
        }
      }
    }
    
    `;
}

function createLoanApplicationDocumentGraphQL() {
  return `
    mutation{
      createDocument(fileInFolderIdentifier:"/Test"
      repositoryIdentifier:"${appConfig.os}"
      classIdentifier:"LoanApplicationDocument"
        documentProperties:{
          name:"LoanApplication2"
          properties:[
            {LoanApplicationNumber:101}
            {LenderName:"HDFC bank"}
            {BorrowerName:"John"}
          ]
        }
        checkinAction: {checkinMinorVersion:false}
      ) {
        id
        name
        className
      }  
    }`;
}
function createLenderDocumentGraphQL() {
  return `
      mutation{
        createDocument(fileInFolderIdentifier:"/Test"
        repositoryIdentifier:"${appConfig.os}"
        classIdentifier:"Lender"
          documentProperties:{
            name:"Lender doc2"
            properties:[
              {LenderName:"HDFC bank"}
            ]
          }
          checkinAction: {checkinMinorVersion:false}
        ) {
          id
          name
          className
        }      
      }
      `;
}
