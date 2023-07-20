#  Licensed Materials - Property of IBM (c) Copyright IBM Corp. 2023 All Rights Reserved.
 
#  US Government Users Restricted Rights - Use, duplication or disclosure restricted by GSA ADP Schedule Contract with
#  IBM Corp.
 
#  DISCLAIMER OF WARRANTIES :
 
#  Permission is granted to copy and modify this Sample code, and to distribute modified versions provided that both the
#  copyright notice, and this permission notice and warranty disclaimer appear in all copies and modified versions.
 
#  THIS SAMPLE CODE IS LICENSED TO YOU AS-IS. IBM AND ITS SUPPLIERS AND LICENSORS DISCLAIM ALL WARRANTIES, EITHER
#  EXPRESS OR IMPLIED, IN SUCH SAMPLE CODE, INCLUDING THE WARRANTY OF NON-INFRINGEMENT AND THE IMPLIED WARRANTIES OF
#  MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE. IN NO EVENT WILL IBM OR ITS LICENSORS OR SUPPLIERS BE LIABLE FOR
#  ANY DAMAGES ARISING OUT OF THE USE OF OR INABILITY TO USE THE SAMPLE CODE, DISTRIBUTION OF THE SAMPLE CODE, OR
#  COMBINATION OF THE SAMPLE CODE WITH ANY OTHER CODE. IN NO EVENT SHALL IBM OR ITS LICENSORS AND SUPPLIERS BE LIABLE
#  FOR ANY LOST REVENUE, LOST PROFITS OR DATA, OR FOR DIRECT, INDIRECT, SPECIAL, CONSEQUENTIAL, INCIDENTAL OR PUNITIVE
#  DAMAGES, HOWEVER CAUSED AND REGARDLESS OF THE THEORY OF LIABILITY, EVEN IF IBM OR ITS LICENSORS OR SUPPLIERS HAVE
#  BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
 


import glob
import os
import requests
import uuid
import argparse
import config
API_CALLS_COUNT = 0


def generateMutation(payload):
    global API_CALLS_COUNT

    headers = {
    'Authorization': 'Bearer ' + TOKEN,
    'Content-Type': 'application/json',
    'ECM-CS-XSRF-Token': XSRF_TOKEN
    }
    cookies = {
        'ECM-CS-XSRF-Token': XSRF_TOKEN
    }

    response = requests.post(url=config.GQL_URL,headers=headers, data=payload, cookies=cookies)
    API_CALLS_COUNT+=1
    print(response.text)

def generateMultipartMutation(payload, file):
    global API_CALLS_COUNT
    cookies = {
        'ECM-CS-XSRF-Token': XSRF_TOKEN
    }
    headers = {
        'ECM-CS-XSRF-Token': XSRF_TOKEN,
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.request("POST", config.GQL_URL, headers=headers, data=payload, files=file, cookies=cookies)

    API_CALLS_COUNT+=1
    print(response.text)

def uploadFile(fileName, localFilePath, repoPath):
    #Folder
    if (os.path.isdir(localFilePath)):
        print("create folder: " + localFilePath)
        payload = "{\"query\":\"   mutation {\\r\\n    createFolder(\\r\\n      repositoryIdentifier: \\\"%s\\\",\\r\\n      folderProperties: {\\r\\n        name: \\\"%s\\\"\\r\\n        parent: {\\r\\n          identifier: \\\"%s\\\"\\r\\n        }\\r\\n      }\\r\\n    ) {\\r\\n        className\\r\\n        id\\r\\n        name\\r\\n        creator\\r\\n        dateCreated\\r\\n        lastModifier\\r\\n        dateLastModified\\r\\n        pathName\\r\\n        properties(includes: [\\\"IsHiddenContainer\\\", \\\"DateCreated\\\", \\\"Creator\\\"]) {\\r\\n        id\\r\\n        label\\r\\n        type\\r\\n        cardinality\\r\\n        value\\r\\n        }\\r\\n    }\\r\\n    }\",\"variables\":{}}" % (config.OS_NAME, fileName, repoPath)
        generateMutation(payload)
        newRepoPath=repoPath+fileName+"\/"
        for filePath in glob.glob(localFilePath+'/*'):
                fileName = os.path.basename(filePath)
                uploadFile(fileName, filePath, newRepoPath)
    #Content Document
    else:
        print("creat document: " + localFilePath)
        file=[('contvar',(fileName,open(localFilePath,'rb'),'multipart/form-data'))]
        payload = {
                'graphql': '{"query":"mutation ($contvar:String) {createDocument(repositoryIdentifier:\\\"%s\\\" fileInFolderIdentifier: \\\"%s\\\" documentProperties: {name: \\"%s\\" content:$contvar} checkinAction: {} ) { id name } }", "variables":{"contvar":null} }' % (config.OS_NAME, repoPath, fileName)
                }
        generateMultipartMutation(payload, file)


def fetchToken():
    global API_CALLS_COUNT

    # API KEY AUTH
    payload = {}
    headers = {
    'X-IBM-Client-Id': config.SERVICE_USER_ID,
    'X-IBM-Client-Secret': config.SERVICE_USER_API_KEY,
    }

    response = requests.request("GET", config.APIC_TOKEN_URL, headers=headers, data=payload)

    API_CALLS_COUNT+=1
    print(response.json())

    return (response.json()["token"])

def createSpanFolders(curDepth, depth, span, folderPath):
    if(curDepth == depth):
        return
    for idxSpan in range(span):
        folderName = "ApiLevel" + "{:02d}".format(idxSpan)
        newFolderPath = folderPath+folderName+"\/"
        payload = "{\"query\":\"   mutation {\\r\\n    createFolder(\\r\\n      repositoryIdentifier: \\\"%s\\\",\\r\\n      folderProperties: {\\r\\n        name: \\\"%s\\\"\\r\\n        parent: {\\r\\n          identifier: \\\"%s\\\"\\r\\n        }\\r\\n      }\\r\\n    ) {\\r\\n        className\\r\\n        id\\r\\n        name\\r\\n        creator\\r\\n        dateCreated\\r\\n        lastModifier\\r\\n        dateLastModified\\r\\n        pathName\\r\\n        properties(includes: [\\\"IsHiddenContainer\\\", \\\"DateCreated\\\", \\\"Creator\\\"]) {\\r\\n        id\\r\\n        label\\r\\n        type\\r\\n        cardinality\\r\\n        value\\r\\n        }\\r\\n    }\\r\\n    }\",\"variables\":{}}" % (config.OS_NAME, folderName, folderPath)
        generateMutation(payload)
        createSpanFolders(curDepth+1, depth, span, newFolderPath)

def deleteSpanFolders(curDepth, depth, span, folderPath):
    if(curDepth == depth):
        return
    for idxSpan in range(span):
        folderName = "ApiLevel" + "{:02d}".format(idxSpan)
        newFolderPath = folderPath+folderName+"\/"
        payload = "{\"query\":\"mutation {\\r\\n  deleteFolder(\\r\\n\\trepositoryIdentifier:\\\"%s\\\", \\r\\n\\tidentifier:\\\"%s\\\") {\\r\\n    id\\r\\n    name\\r\\n    pathName\\r\\n    objectReference {\\r\\n      repositoryIdentifier\\r\\n      classIdentifier\\r\\n      identifier\\r\\n    }\\r\\n  }\\r\\n}\",\"variables\":{}}" % (config.OS_NAME, folderPath+folderName)
        deleteSpanFolders(curDepth+1, depth, span, newFolderPath)
        generateMutation(payload)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                prog='GraphQL Python Sample',
                description='''Generates GQL API calls:
                1) Create folders with inputted span and depth
                2) upload content-upload folder and all content in it:''',
                epilog='Make sure to edit config.py to match system\'s information')
    global XSRF_TOKEN
    global TOKEN
    #Note that it is possible to fetch XSRF token from graphql ping URL without generating a token locally.
    XSRF_TOKEN = str(uuid.uuid4())
    TOKEN = fetchToken()

    function = None
    while(function != '1' and function != '2'):
        function = input("Enter the corresponding number for the desired functionality:\n1) Generate API Calls\n2) Upload Folder with content\n")
        if (function == "1"):
            iterations = int(input("Enter iteration (non-zero number):\n"))
            span = int(input("Enter span (non-zero number):\n"))
            depth = int(input("Enter depth (non-zero number)\n"))
            if((iterations or span or depth) == 0):
                print("Unexpected input")
                exit()
            for iteration in range(iterations):
                curDepth = 0
                folderName = "ApiLevel00"
                folderPath = "\/"
                #create top level folder
                payload = "{\"query\":\"   mutation {\\r\\n    createFolder(\\r\\n      repositoryIdentifier: \\\"%s\\\",\\r\\n      folderProperties: {\\r\\n        name: \\\"%s\\\"\\r\\n        parent: {\\r\\n          identifier: \\\"%s\\\"\\r\\n        }\\r\\n      }\\r\\n    ) {\\r\\n        className\\r\\n        id\\r\\n        name\\r\\n        creator\\r\\n        dateCreated\\r\\n        lastModifier\\r\\n        dateLastModified\\r\\n        pathName\\r\\n        properties(includes: [\\\"IsHiddenContainer\\\", \\\"DateCreated\\\", \\\"Creator\\\"]) {\\r\\n        id\\r\\n        label\\r\\n        type\\r\\n        cardinality\\r\\n        value\\r\\n        }\\r\\n    }\\r\\n    }\",\"variables\":{}}" % (config.OS_NAME, folderName, folderPath)
                generateMutation(payload)

                newFolderPath = "/ApiLevel00/"
                createSpanFolders(curDepth+1, depth, span, newFolderPath)
                deleteSpanFolders(curDepth+1, depth, span, newFolderPath)

                #delete top level folder
                payload = "{\"query\":\"mutation {\\r\\n  deleteFolder(\\r\\n\\trepositoryIdentifier:\\\"%s\\\", \\r\\n\\tidentifier:\\\"%s\\\") {\\r\\n    id\\r\\n    name\\r\\n    pathName\\r\\n    objectReference {\\r\\n      repositoryIdentifier\\r\\n      classIdentifier\\r\\n      identifier\\r\\n    }\\r\\n  }\\r\\n}\",\"variables\":{}}" % (config.OS_NAME, folderPath+folderName)
                generateMutation(payload)
            print("TOTAL COUNT FOR APIS: %s" % str(API_CALLS_COUNT))
        elif (function == "2"):
            # fileName = "content-upload"
            # localFilePath = os.getcwd()+"/"+fileName
            if (not os.path.exists(config.FILE_PATH)):
                print("Invalid File Path")
                exit()
            localFilePath = config.FILE_PATH
            if( localFilePath[-1] == ("/" or "\\") ):
                localFilePath=localFilePath[:-1]
            fileName = os.path.basename(localFilePath)
            uploadFile(fileName, localFilePath, "\/")
        else:
            print("Unexpected input")
    exit()

