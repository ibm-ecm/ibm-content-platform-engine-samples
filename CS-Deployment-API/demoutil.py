#  Licensed Materials - Property of IBM (c) Copyright IBM Corp. 2024 All Rights Reserved.

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

from csdeploy import GraphqlRequest
from csdeploy import ObjectSelection
from csdeploy import GraphqlConnection, ExportSelectionUtil


class ClassDefinitionsSelector:
    def __init__(
        self,
        os_name: str,
        gqlConnection: GraphqlConnection,
        NumberOfClassesToRetrieve: int = 500,
    ) -> None:
        self.os_name = os_name
        self.gqlConnection = gqlConnection
        self.selections: list[ObjectSelection] = []
        self.NumberOfClassesToRetrieve = NumberOfClassesToRetrieve

    def prompt_selection(self) -> list[ObjectSelection]:
        gql_request = GraphqlRequest(self.gqlConnection)
        classes_response = ExportSelectionUtil(
            gql_request=gql_request, object_store_name=self.os_name
        ).query_class_definitions()
        class_objs_list = [
            class_obj
            for class_obj in classes_response["data"]["repositoryObjects"][
                "independentObjects"
            ]
        ]
        # Exit on no classes found
        if not class_objs_list:
            print("No classes detected")
            return
        class_names_list = [class_obj["displayName"] for class_obj in class_objs_list]

        for idx, class_name in enumerate(class_names_list, start=0):
            if idx > len(class_objs_list):
                print("Invalid index")
                return
            print(idx, "-", class_name)
        str_input = input("Enter multiple values with comma or just a single value \n")
        strlist = str_input.split(",")
        list1 = []
        for item in strlist:
            list1.append(int(item))
        # Get class definition to export dependencies
        class_def_sels = []
        i = 0
        while i < len(list1):
            response_clsdef = class_objs_list[int(list1[i])]
            class_def_sel = ObjectSelection(
                id=response_clsdef["id"], label=response_clsdef["displayName"]
            )
            class_def_sels.append(class_def_sel)
            i += 1
        self.selections = class_def_sels
        return self.selections
