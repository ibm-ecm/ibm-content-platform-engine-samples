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
from enum import Enum

NULL_VALUE = object()

class FieldArgument:
    def __init__(self, argName:str, argVal:any) -> None:
        self.argName:str = argName
        self.argVal:any = argVal

class GraphqlPart:
    def __init__(self) -> None:
        pass
    def to_graphql(self, fieldsOnly:bool=False) -> str:
        return ""
    def _serializeVal(self, val) -> str:
        strval = ""
        if val is NULL_VALUE:
            strval = "null"
        elif isinstance(val, str):
            strval = "\"" + val + "\""
        elif isinstance(val, bool):
            strval = str(val).lower()
        elif isinstance(val, int):
            strval = str(val)
        elif isinstance(val, float):
            strval = str(val)
        elif isinstance(val, Enum):
            strval = val.name
        elif isinstance(val, GraphqlPart):
            strval = val.to_graphql()
        elif isinstance(val, list):
            strparts = []
            strparts.append("[ ")
            for litem in val:
                listrval = self._serializeVal(litem)
                strparts.append(listrval + " ")
            strparts.append("]")
            strval = "".join(strparts)
        return strval

class InlineFragment(GraphqlPart):
    def __init__(self, onOutput:GraphqlPart) -> None:
        super().__init__()
        self.onOutput:GraphqlPart = onOutput
    def to_graphql(self) -> str:
        return "... on " + type(self.onOutput).__name__ + self.onOutput.to_graphql()

class InputItem:
    def __init__(self, fieldName:str, fieldValue) -> None:
        self.fieldName = fieldName
        self.fieldValue = fieldValue

class InputPart(GraphqlPart):
    def __init__(self) -> None:
        super().__init__()
        self.inputItems:list[InputItem] = []
    def inputField(self, name, value) -> "InputPart":
        ifld = InputItem(fieldName=name, fieldValue=value)
        self.inputItems.append(ifld)
        return self
    def to_graphql(self, fieldsOnly:bool=False) -> str:
        # super method is signature only. No need to call.
        strparts = []
        if not fieldsOnly:
            strparts.append(" {")
        self._serializeInputItems(self.inputItems)
        if not fieldsOnly:
            strparts.append(" }")
        return "".join(strparts)
    def _serializeInputItems(self, items:list[InputItem]) -> str:
        strparts = []
        for item in items:
            strparts.append(" " + item.fieldName + ": " + self._serializeVal(item.fieldValue))
        return "".join(strparts)
    def _serializeFields(self, names:list[str], values:list) -> str:
        items:list[InputItem] = []
        for name, value in zip(names, values):
            if value is not None:
                items.append(InputItem(fieldName=name, fieldValue=value))
        return self._serializeInputItems(items)



class OutputItem:
    def __init__(self, fieldName:str=None, fieldOutput:GraphqlPart=None, fieldArguments:list[FieldArgument]=None, fieldAlias:str=None, 
                 inlineFragment:InlineFragment=None) -> None:
        self.fieldName:str = fieldName
        self.fieldOutput:GraphqlPart = fieldOutput
        self.fieldArguments:list[FieldArgument] = fieldArguments
        self.fieldAlias:str = fieldAlias
        self.inlineFragment:InlineFragment = inlineFragment

class OutputPart(GraphqlPart):
    def __init__(self) -> None:
        super().__init__()
        self.outputItems:list[OutputItem] = [] 
    def inlineFragment(self, frag:InlineFragment) -> "OutputPart":
        self.outputItems.append(OutputItem(inlineFragment=frag))
        return self
    def field(self, fieldName:str, fieldArguments:list[FieldArgument]=None, fieldAlias:str=None, fieldOutput:GraphqlPart=None) -> "OutputPart":
        self.outputItems.append(OutputItem(fieldName=fieldName, fieldArguments=fieldArguments, \
                                           fieldAlias=fieldAlias, fieldOutput=fieldOutput))
        return self
    def to_graphql(self:"OutputPart") -> str:
        # super method is signature only. No need to call.
        strparts = []
        strparts.append(" {")
        for oitem in self.outputItems:
            if oitem.fieldName is not None:
                strparts.append(" ")
                if oitem.fieldAlias is not None:
                    strparts.append(oitem.fieldAlias + ": ")
                strparts.append(oitem.fieldName)
                if oitem.fieldArguments is not None and len(oitem.fieldArguments) != 0:
                    strparts.append("(")
                    for farg in oitem.fieldArguments:
                        strparts.append(" " + farg.argName + ": ")
                        strparts.append(self._serializeVal(farg.argVal))
                    strparts.append(")")
                if oitem.fieldOutput is not None:
                    strparts.append(oitem.fieldOutput.to_graphql())
            elif oitem.inlineFragment is not None:
                strparts.append(" ")
                strparts.append(oitem.inlineFragment.to_graphql())
        strparts.append(" }")
        return "".join(strparts)
    

