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
from csdeploy.gqlschema.gqlcore import OutputPart, FieldArgument, OutputItem
from csdeploy.gqlschema.adminbase import PropertyTemplate, ClassDefinition, ChoiceList
from csdeploy.gqlschema.propertybase import TypeID
from csdeploy.gqlschema.admin import PropertyTemplatePropertiesInput, ClassDefinitionPropertiesInput, ChoiceListPropertiesInput

class Query(OutputPart):
    def __init__(self) -> None:
        super().__init__()
    def field_admPropertyTemplate(self, repositoryIdentifier:str, identifier:str, alias:str=None, fieldOutput:PropertyTemplate = None) -> "Query":
        args:list[FieldArgument] = []
        args.append(FieldArgument(argName="repositoryIdentifier", argVal=repositoryIdentifier))
        args.append(FieldArgument(argName="identifier", argVal=identifier))
        self.outputItems.append(OutputItem(fieldName="admPropertyTemplate", fieldArguments=args, fieldAlias=alias, fieldOutput=fieldOutput))
        return self
    def field_admClassDefinition(self, repositoryIdentifier:str, identifier:str, alias:str=None, fieldOutput:ClassDefinition=None) -> "Query":
        args:list[FieldArgument] = []
        args.append(FieldArgument(argName="repositoryIdentifier", argVal=repositoryIdentifier))
        args.append(FieldArgument(argName="identifier", argVal=identifier))
        self.outputItems.append(OutputItem(fieldName="admClassDefinition", fieldArguments=args, fieldAlias=alias, fieldOutput=fieldOutput))
        return self
    def field_choiceList(self, repositoryIdentifier: str, identifier:str, alias:str=None, fieldOutput: ChoiceList = None) -> "Query":
        args:list[FieldArgument] = []
        args.append(FieldArgument(argName="repositoryIdentifier", argVal=repositoryIdentifier))
        args.append(FieldArgument(argName="identifier", argVal=identifier))
        self.outputItems.append(OutputItem(fieldName="choiceList", fieldArguments=args, fieldAlias=alias, fieldOutput=fieldOutput))
        return self
    
    def to_query(self, includeQueryKeyword=False) -> str:
        # TODO: additional options for operation name and arguments
        strparts:list[str] = []
        if includeQueryKeyword:
            strparts.append("query ")
        strparts.append(self.to_graphql())
        return "".join(strparts)

class Mutation(OutputPart):
    def __init__(self) -> None:
        super().__init__()
    def field_admCreatePropertyTemplate(self, repositoryIdentifier:str, dataType:TypeID, id:str=None, 
                                        propertyTemplateProperties:PropertyTemplatePropertiesInput=None, alias=None, 
                                        fieldOutput:PropertyTemplate=None) -> "Mutation":
        args:list[FieldArgument] = []
        args.append(FieldArgument(argName="repositoryIdentifier", argVal=repositoryIdentifier))
        args.append(FieldArgument(argName="dataType", argVal=dataType))
        if id is not None:
            args.append(FieldArgument(argName="id", argVal=id))
        if propertyTemplateProperties is not None:
            args.append(FieldArgument(argName="propertyTemplateProperties", argVal=propertyTemplateProperties))
        self.outputItems.append(OutputItem(fieldName="admCreatePropertyTemplate", fieldArguments=args, fieldAlias=alias, fieldOutput=fieldOutput))
        return self
    def field_admUpdatePropertyTemplate(self, repositoryIdentifier:str, identifier:str, updateSequenceNumber:int=None,
                                        propertyTemplateProperties:PropertyTemplatePropertiesInput=None, alias=None, 
                                        fieldOutput:PropertyTemplate=None) -> "Mutation":
        args:list[FieldArgument] = []
        args.append(FieldArgument(argName="repositoryIdentifier", argVal=repositoryIdentifier))
        args.append(FieldArgument(argName="identifier", argVal=identifier))
        if updateSequenceNumber is not None:
            args.append(FieldArgument(argName="updateSequenceNumber", argVal=updateSequenceNumber))
        if propertyTemplateProperties is not None:
            args.append(FieldArgument(argName="propertyTemplateProperties", argVal=propertyTemplateProperties))
        self.outputItems.append(OutputItem(fieldName="admUpdatePropertyTemplate", fieldArguments=args, fieldAlias=alias, fieldOutput=fieldOutput))
        return self
    def field_admDeletePropertyTemplate(self, repositoryIdentifier:str, identifier:str, updateSequenceNumber:int=None,
                                        alias=None, fieldOutput:PropertyTemplate=None) -> "Mutation":
        args:list[FieldArgument] = []
        args.append(FieldArgument(argName="repositoryIdentifier", argVal=repositoryIdentifier))
        args.append(FieldArgument(argName="identifier", argVal=identifier))
        if updateSequenceNumber is not None:
            args.append(FieldArgument(argName="updateSequenceNumber", argVal=updateSequenceNumber))
        self.outputItems.append(OutputItem(fieldName="admDeletePropertyTemplate", fieldArguments=args, fieldAlias=alias, fieldOutput=fieldOutput))
        return self
    def field_admCreateClassDefinition(self, repositoryIdentifier:str, superclassIdentifier:str, id:str=None,
                                       classDefinitionProperties:ClassDefinitionPropertiesInput=None,
                                       alias=None, fieldOutput:ClassDefinition=None) -> "Mutation":
        args:list[FieldArgument] = []
        args.append(FieldArgument(argName="repositoryIdentifier", argVal=repositoryIdentifier))
        args.append(FieldArgument(argName="superclassIdentifier", argVal=superclassIdentifier))
        if id is not None:
            args.append(FieldArgument(argName="id", argVal=id))
        if classDefinitionProperties is not None:
            args.append(FieldArgument(argName="classDefinitionProperties", argVal=classDefinitionProperties))
        self.outputItems.append(OutputItem(fieldName="admCreateClassDefinition", fieldArguments=args, fieldAlias=alias, fieldOutput=fieldOutput))
        return self
    def field_admUpdateClassDefinition(self, repositoryIdentifier:str, identifier:str, updateSequenceNumber:int=None,
                                       classDefinitionProperties:ClassDefinitionPropertiesInput=None,
                                       alias=None, fieldOutput:ClassDefinition=None) -> "Mutation":
        args:list[FieldArgument] = []
        args.append(FieldArgument(argName="repositoryIdentifier", argVal=repositoryIdentifier))
        args.append(FieldArgument(argName="identifier", argVal=identifier))
        if updateSequenceNumber is not None:
            args.append(FieldArgument(argName="updateSequenceNumber", argVal=updateSequenceNumber))
        if classDefinitionProperties is not None:
            args.append(FieldArgument(argName="classDefinitionProperties", argVal=classDefinitionProperties))
        self.outputItems.append(OutputItem(fieldName="admUpdateClassDefinition", fieldArguments=args, fieldAlias=alias, fieldOutput=fieldOutput))
        return self
    def field_admDeleteClassDefinition(self, repositoryIdentifier:str, identifier:str, updateSequenceNumber:int=None,
                                       alias=None, fieldOutput:ClassDefinition=None) -> "Mutation":
        args:list[FieldArgument] = []
        args.append(FieldArgument(argName="repositoryIdentifier", argVal=repositoryIdentifier))
        args.append(FieldArgument(argName="identifier", argVal=identifier))
        if updateSequenceNumber is not None:
            args.append(FieldArgument(argName="updateSequenceNumber", argVal=updateSequenceNumber))
        self.outputItems.append(OutputItem(fieldName="admUpdateClassDefinition", fieldArguments=args, fieldAlias=alias, fieldOutput=fieldOutput))
        return self
    def field_admCreateChoiceList(self, repositoryIdentifier:str, id:str=None,
                                       choiceListProperties:ChoiceListPropertiesInput=None,
                                       alias=None, fieldOutput:ChoiceList=None) -> "Mutation":
        args:list[FieldArgument] = []
        args.append(FieldArgument(argName="repositoryIdentifier", argVal=repositoryIdentifier))
        
        if id is not None:
            args.append(FieldArgument(argName="id", argVal=id))
        if choiceListProperties is not None:
            args.append(FieldArgument(argName="choiceListProperties", argVal=choiceListProperties))
        self.outputItems.append(OutputItem(fieldName="admCreateChoiceList", fieldArguments=args, fieldAlias=alias, fieldOutput=fieldOutput))
        return self
    def field_admUpdateChoiceList(self, repositoryIdentifier:str, identifier:str, updateSequenceNumber:int=None,
                                        choiceListProperties:ChoiceListPropertiesInput=None, alias=None, 
                                        fieldOutput:ChoiceList=None) -> "Mutation":
        args:list[FieldArgument] = []
        args.append(FieldArgument(argName="repositoryIdentifier", argVal=repositoryIdentifier))
        args.append(FieldArgument(argName="identifier", argVal=identifier))
        if updateSequenceNumber is not None:
            args.append(FieldArgument(argName="updateSequenceNumber", argVal=updateSequenceNumber))
        if choiceListProperties is not None:
            args.append(FieldArgument(argName="choiceListProperties", argVal=choiceListProperties))
        self.outputItems.append(OutputItem(fieldName="admUpdateChoiceList", fieldArguments=args, fieldAlias=alias, fieldOutput=fieldOutput))
        return self
    def to_query(self) -> str:
        # TODO: additional options for operation name and arguments
        strparts:list[str] = []
        # Always include mutation keyword
        strparts.append("mutation ")
        strparts.append(self.to_graphql())
        return "".join(strparts)

