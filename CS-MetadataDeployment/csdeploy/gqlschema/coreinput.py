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
from csdeploy.gqlschema.gqlcore import InputPart

class DependentItemReferenceInput(InputPart):
    def __init__(self, id:str=None, identifier:str=None, originalIndex:int=None, sequenceNumber:int=None) -> None:
        super().__init__()
        self.id:str = id
        self.identifier:str = identifier
        self.originalIndex:int = originalIndex
        self.sequenceNumber:int = sequenceNumber
    def to_graphql(self, fieldsOnly:bool=False) -> str:
        strparts:list[str] = []
        if not fieldsOnly:
            strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["id", "identifier", "originalIndex", "sequenceNumber"]
        values = [self.id, self.identifier, self.originalIndex, self.sequenceNumber]
        strparts.append(self._serializeFields(names, values))
        if not fieldsOnly:
            strparts.append(" }")
        return "".join(strparts)

class InsertDependentActionInput(InputPart):
    def __init__(self, classIdentifier:str=None, newIndex:int=None) -> None:
        super().__init__()
        self.classIdentifier:str = classIdentifier
        self.newIndex:int = newIndex
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["classIdentifier", "newIndex"]
        values = [self.classIdentifier, self.newIndex]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)

class UpdateDependentActionInput(InputPart):
    def __init__(self, itemReference:DependentItemReferenceInput=None) -> None:
        super().__init__()
        self.itemReference:DependentItemReferenceInput = itemReference
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["itemReference"]
        values = [self.itemReference]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)

class MoveDependentActionInput(InputPart):
    def __init__(self, itemReference:DependentItemReferenceInput=None, newIndex:int=None) -> None:
        super().__init__()
        self.itemReference:DependentItemReferenceInput = itemReference
        self.newIndex:int = newIndex
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["itemReference", "newIndex"]
        values = [self.itemReference, self.newIndex]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)

class DeleteDependentActionInput(InputPart):
    def __init__(self, itemReference:DependentItemReferenceInput=None) -> None:
        super().__init__()
        self.itemReference:DependentItemReferenceInput = itemReference
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["itemReference"]
        values = [self.itemReference]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)

class BaseDependentObjectInput(InputPart):
    def __init__(self, insertAction:InsertDependentActionInput=None, updateAction:UpdateDependentActionInput=None,
                 moveAction:MoveDependentActionInput=None, deleteAction:DeleteDependentActionInput=None) -> None:
        super().__init__()
        self.insertAction:InsertDependentActionInput = insertAction
        self.updateAction:UpdateDependentActionInput = updateAction
        self.moveAction:MoveDependentActionInput = moveAction
        self.deleteAction:DeleteDependentActionInput = deleteAction
    def to_graphql(self, fieldsOnly:bool=False) -> str:
        strparts:list[str] = []
        if not fieldsOnly:
            strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["insertAction", "updateAction", "moveAction", "deleteAction"]
        values = [self.insertAction, self.updateAction, self.moveAction, self.deleteAction]
        strparts.append(self._serializeFields(names, values))
        if not fieldsOnly:
            strparts.append(" }")
        return "".join(strparts)
        


