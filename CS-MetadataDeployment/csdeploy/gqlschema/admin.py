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
from csdeploy.gqlschema.gqlcore import InputPart, OutputItem
from csdeploy.gqlschema.corebase import ObjectReferenceInput
from csdeploy.gqlschema.adminbase import PropertyTemplate, PropertyDefinition, DurationUnits, ChoiceType
from csdeploy.gqlschema.coreinput import BaseDependentObjectInput, InsertDependentActionInput, UpdateDependentActionInput, MoveDependentActionInput, DeleteDependentActionInput
from csdeploy.gqlschema.propertybase import Cardinality, PropertySettability, TypeID

class PropertyTemplateString(PropertyTemplate):
    def __init__(self) -> None:
        super().__init__()
    def field_maximumLengthString(self, alias=None) -> "PropertyTemplateString":
        self.outputItems.append(OutputItem(fieldName="maximumLengthString", fieldAlias=alias))
        return self
    def field_propertyDefaultString(self, alias=None) -> "PropertyTemplateString":
        self.outputItems.append(OutputItem(fieldName="propertyDefaultString", fieldAlias=alias))
        return self

class PropertyTemplateBinary(PropertyTemplate):
    def __init__(self) -> None:
        super().__init__()
    def field_isReadProtected(self, alias=None) -> "PropertyTemplateBinary":
        self.outputItems.append(OutputItem(fieldName="isReadProtected", fieldAlias=alias))
        return self
    def field_maximumLengthBinary(self, alias=None) -> "PropertyTemplateBinary":
        self.outputItems.append(OutputItem(fieldName="maximumLengthBinary", fieldAlias=alias))
        return self
    def field_propertyDefaultBinary(self, alias=None) -> "PropertyTemplateBinary":
        self.outputItems.append(OutputItem(fieldName="propertyDefaultBinary", fieldAlias=alias))
        return self

class PropertyTemplateBoolean(PropertyTemplate):
    def __init__(self) -> None:
        super().__init__()
    def field_propertyDefaultBoolean(self, alias=None) -> "PropertyTemplateBoolean":
        self.outputItems.append(OutputItem(fieldName="propertyDefaultBoolean", fieldAlias=alias))
        return self

class PropertyTemplateDateTime(PropertyTemplate):
    def __init__(self) -> None:
        super().__init__()
    def field_isDateOnly(self, alias=None) -> "PropertyTemplateDateTime":
        self.outputItems.append(OutputItem(fieldName="isDateOnly", fieldAlias=alias))
        return self
    def field_propertyDefaultDateTime(self, alias=None) -> "PropertyTemplateDateTime":
        self.outputItems.append(OutputItem(fieldName="propertyDefaultDateTime", fieldAlias=alias))
        return self
    def field_propertyMaximumDateTime(self, alias=None) -> "PropertyTemplateDateTime":
        self.outputItems.append(OutputItem(fieldName="propertyMaximumDateTime", fieldAlias=alias))
        return self
    def field_propertyMinimumDateTime(self, alias=None) -> "PropertyTemplateDateTime":
        self.outputItems.append(OutputItem(fieldName="propertyMinimumDateTime", fieldAlias=alias))
        return self

class PropertyTemplateFloat64(PropertyTemplate):
    def __init__(self) -> None:
        super().__init__()
    def field_propertyDefaultFloat64(self, alias=None) -> "PropertyTemplateFloat64":
        self.outputItems.append(OutputItem(fieldName="propertyDefaultFloat64", fieldAlias=alias))
        return self
    def field_propertyMaximumFloat64(self, alias=None) -> "PropertyTemplateFloat64":
        self.outputItems.append(OutputItem(fieldName="propertyMaximumFloat64", fieldAlias=alias))
        return self
    def field_propertyMinimumFloat64(self, alias=None) -> "PropertyTemplateFloat64":
        self.outputItems.append(OutputItem(fieldName="propertyMinimumFloat64", fieldAlias=alias))
        return self

class PropertyTemplateId(PropertyTemplate):
    def __init__(self) -> None:
        super().__init__()
    def field_propertyDefaultId(self, alias=None) -> "PropertyTemplateId":
        self.outputItems.append(OutputItem(fieldName="propertyDefaultId", fieldAlias=alias))
        return self

class PropertyTemplateInteger32(PropertyTemplate):
    def __init__(self) -> None:
        super().__init__()
    def field_propertyDefaultInteger32(self, alias=None) -> "PropertyTemplateInteger32":
        self.outputItems.append(OutputItem(fieldName="propertyDefaultInteger32", fieldAlias=alias))
        return self
    def field_propertyMaximumInteger32(self, alias=None) -> "PropertyTemplateInteger32":
        self.outputItems.append(OutputItem(fieldName="propertyMaximumInteger32", fieldAlias=alias))
        return self
    def field_propertyMinimumInteger32(self, alias=None) -> "PropertyTemplateInteger32":
        self.outputItems.append(OutputItem(fieldName="propertyMinimumInteger32", fieldAlias=alias))
        return self

class PropertyTemplateObject(PropertyTemplate):
    def __init__(self) -> None:
        super().__init__()
    def field_allowsForeignObject(self, alias=None) -> "PropertyTemplateObject":
        self.outputItems.append(OutputItem(fieldName="allowsForeignObject", fieldAlias=alias))
        return self
    
class PropertyDefinitionBinary(PropertyDefinition):
    def __init__(self) -> None:
        super().__init__()
    def field_isReadProtected(self, alias=None) -> "PropertyDefinitionBinary":
        self.outputItems.append(OutputItem(fieldName="isReadProtected", fieldAlias=alias))
        return self
    def field_maximumLengthBinary(self, alias=None) -> "PropertyDefinitionBinary":
        self.outputItems.append(OutputItem(fieldName="maximumLengthBinary", fieldAlias=alias))
        return self
    def field_propertyDefaultBinary(self, alias=None) -> "PropertyDefinitionBinary":
        self.outputItems.append(OutputItem(fieldName="propertyDefaultBinary", fieldAlias=alias))
        return self

class PropertyDefinitionBoolean(PropertyDefinition):
    def __init__(self) -> None:
        super().__init__()
    def field_propertyDefaultBoolean(self, alias=None) -> "PropertyDefinitionBoolean":
        self.outputItems.append(OutputItem(fieldName="propertyDefaultBoolean", fieldAlias=alias))
        return self

class PropertyDefinitionDateTime(PropertyDefinition):
    def __init__(self) -> None:
        super().__init__()
    def field_isDateOnly(self, alias=None) -> "PropertyDefinitionDateTime":
        self.outputItems.append(OutputItem(fieldName="isDateOnly", fieldAlias=alias))
        return self
    def field_propertyDefaultDateTime(self, alias=None) -> "PropertyDefinitionDateTime":
        self.outputItems.append(OutputItem(fieldName="propertyDefaultDateTime", fieldAlias=alias))
        return self
    def field_propertyMaximumDateTime(self, alias=None) -> "PropertyDefinitionDateTime":
        self.outputItems.append(OutputItem(fieldName="propertyMaximumDateTime", fieldAlias=alias))
        return self
    def field_propertyMinimumDateTime(self, alias=None) -> "PropertyDefinitionDateTime":
        self.outputItems.append(OutputItem(fieldName="propertyMinimumDateTime", fieldAlias=alias))
        return self

class PropertyDefinitionFloat64(PropertyDefinition):
    def __init__(self) -> None:
        super().__init__()
    def field_propertyDefaultFloat64(self, alias=None) -> "PropertyDefinitionFloat64":
        self.outputItems.append(OutputItem(fieldName="propertyDefaultFloat64", fieldAlias=alias))
        return self
    def field_propertyMaximumFloat64(self, alias=None) -> "PropertyDefinitionFloat64":
        self.outputItems.append(OutputItem(fieldName="propertyMaximumFloat64", fieldAlias=alias))
        return self
    def field_propertyMinimumFloat64(self, alias=None) -> "PropertyDefinitionFloat64":
        self.outputItems.append(OutputItem(fieldName="propertyMinimumFloat64", fieldAlias=alias))
        return self

class PropertyDefinitionId(PropertyDefinition):
    def __init__(self) -> None:
        super().__init__()
    def field_propertyDefaultId(self, alias=None) -> "PropertyDefinitionId":
        self.outputItems.append(OutputItem(fieldName="propertyDefaultId", fieldAlias=alias))
        return self

class PropertyDefinitionInteger32(PropertyDefinition):
    def __init__(self) -> None:
        super().__init__()
    def field_propertyDefaultInteger32(self, alias=None) -> "PropertyDefinitionInteger32":
        self.outputItems.append(OutputItem(fieldName="propertyDefaultInteger32", fieldAlias=alias))
        return self
    def field_propertyMaximumInteger32(self, alias=None) -> "PropertyDefinitionInteger32":
        self.outputItems.append(OutputItem(fieldName="propertyMaximumInteger32", fieldAlias=alias))
        return self
    def field_propertyMinimumInteger32(self, alias=None) -> "PropertyDefinitionInteger32":
        self.outputItems.append(OutputItem(fieldName="propertyMinimumInteger32", fieldAlias=alias))
        return self

class PropertyDefinitionObject(PropertyDefinition):
    def __int__(self) -> None:
        super().__init__()
    def field_requiredClassId(self, alias=None) -> "PropertyDefinitionObject":
        self.outputItems.append(OutputItem(fieldName="requiredClassId", fieldAlias=alias))
        return self
    def field_reflectivePropertyId(self, alias=None) -> "PropertyDefinitionObject":
        self.outputItems.append(OutputItem(fieldName="reflectivePropertyId", fieldAlias=alias))
        return self

    


class PropertyDefinitionString(PropertyDefinition):
    def __init__(self) -> None:
        super().__init__()
    def field_maximumLengthString(self, alias=None) -> "PropertyDefinitionString":
        self.outputItems.append(OutputItem(fieldName="maximumLengthString", fieldAlias=alias))
        return self
    def field_propertyDefaultString(self, alias=None) -> "PropertyDefinitionString":
        self.outputItems.append(OutputItem(fieldName="propertyDefaultString", fieldAlias=alias))
        return self
    def field_usesLongColumn(self, alias=None) -> "PropertyDefinitionString":
        self.outputItems.append(OutputItem(fieldName="usesLongColumn", fieldAlias=alias))
        return self

class LocalizedStringInput(BaseDependentObjectInput):
    def __init__(self, insertAction:InsertDependentActionInput=None, updateAction:UpdateDependentActionInput=None,
                 moveAction:MoveDependentActionInput=None, deleteAction:DeleteDependentActionInput=None,
                 localeName:str=None, localizedText:str=None) -> None:
        super().__init__(insertAction=insertAction, updateAction=updateAction, 
                         moveAction=moveAction, deleteAction=deleteAction)
        self.localeName:str = localeName
        self.localizedText:str = localizedText
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["localeName", "localizedText"]
        values = [self.localeName, self.localizedText]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)

class LocalizedStringListInput(InputPart):
    def __init__(self, replace:list[LocalizedStringInput]=None, modify:list[LocalizedStringInput]=None) -> None:
        super().__init__()
        self.replace:list[LocalizedStringInput] = replace
        self.modify:list[LocalizedStringInput] = modify
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["replace", "modify"]
        values = [self.replace, self.modify]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)
    
class ChoiceInput(BaseDependentObjectInput):
    def __init__(self, insertAction: InsertDependentActionInput = None, updateAction: UpdateDependentActionInput = None, 
                 moveAction: MoveDependentActionInput = None, deleteAction: DeleteDependentActionInput = None,
                 choiceIntegerValue: int=None, choiceStringValue: str=None, choiceValues: "ChoiceListInput"=None,
                 displayName: str=None, 
                 displayNames: LocalizedStringListInput=None,
                 choiceType: ChoiceType=None) -> None:
        super().__init__(insertAction, updateAction, moveAction, deleteAction)
        self.choiceIntegerValue:int = choiceIntegerValue
        self.choiceStringValue:str = choiceStringValue
        self.choiceValues:ChoiceInput = choiceValues
        self.displayName:str = displayName
        self.displayNames:LocalizedStringListInput = displayNames
        self.choiceType = choiceType
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["choiceIntegerValue", "choiceStringValue", "choiceValues", "displayName", "displayNames", "choiceType"]
        values = [self.choiceIntegerValue, self.choiceStringValue, self.choiceValues, self.displayName, self.displayNames, self.choiceType]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)

class ChoiceListInput(InputPart):
    def __init__(self, replace:list[ChoiceInput]=None, modify:list[ChoiceInput]=None) -> None:
        super().__init__()
        self.replace:list[ChoiceInput] = replace
        self.modify:list[ChoiceInput] = modify
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["replace", "modify"]
        values = [self.replace, self.modify]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)
    


class ChoiceListPropertiesInput(InputPart):
    def __init__(self, 
                 displayName:str=None, descriptiveText: str=None, dataType:TypeID=None,
                 choiceValues: ChoiceListInput=None) -> None:
        super().__init__()
        self.displayName:str = displayName
        self.descriptiveText:str = descriptiveText
        self.dataType:TypeID = dataType
        self.choiceValues = choiceValues
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["displayName", "descriptiveText", "dataType",  
                  "choiceValues"]
        values = [self.displayName, self.descriptiveText, self.dataType, 
                   self.choiceValues]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)
    
class SubPropertyTemplateStringPropertiesInput(InputPart):
    def __init__(self, maximumLengthString:int=None, propertyDefaultString:str=None) -> None:
        super().__init__()
        self.maximumLengthString:int = maximumLengthString
        self.propertyDefaultString:str = propertyDefaultString
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["maximumLengthString", "propertyDefaultString"]
        values = [self.maximumLengthString, self.propertyDefaultString]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)

class SubPropertyTemplateBinaryPropertiesInput(InputPart):
    def __init__(self, isReadProtected:bool=None, maximumLengthBinary:int=None, propertyDefaultBinary:str=None) -> None:
        super().__init__()
        self.isReadProtected:bool = isReadProtected
        self.maximumLengthBinary:int = maximumLengthBinary
        self.propertyDefaultBinary:str = propertyDefaultBinary
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["isReadProtected", "maximumLengthBinary", "propertyDefaultBinary"]
        values = [self.isReadProtected, self.maximumLengthBinary, self.propertyDefaultBinary]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)

class SubPropertyTemplateBooleanPropertiesInput(InputPart):
    def __init__(self, propertyDefaultBoolean:bool=None) -> None:
        super().__init__()
        self.propertyDefaultBoolean:bool = propertyDefaultBoolean
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["propertyDefaultBoolean"]
        values = [self.propertyDefaultBoolean]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)

class SubPropertyTemplateDateTimePropertiesInput(InputPart):
    def __init__(self, propertyDefaultDateTime:str=None, propertyMaximumDateTime:str=None, 
                 propertyMinimumDateTime:str=None) -> None:
        super().__init__()
        self.propertyDefaultDateTime:str = propertyDefaultDateTime
        self.propertyMaximumDateTime:str = propertyMaximumDateTime
        self.propertyMinimumDateTime:str = propertyMinimumDateTime
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["propertyDefaultDateTime", "propertyMaximumDateTime", "propertyMinimumDateTime"]
        values = [self.propertyDefaultDateTime, self.propertyMaximumDateTime, self.propertyMinimumDateTime]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)

class SubPropertyTemplateFloat64PropertiesInput(InputPart):
    def __init__(self, propertyDefaultFloat64:float=None, propertyMaximumFloat64:float=None, 
                 propertyMinimumFloat64:float=None) -> None:
        super().__init__()
        self.propertyDefaultFloat64:float = propertyDefaultFloat64
        self.propertyMaximumFloat64:float = propertyMaximumFloat64
        self.propertyMinimumFloat64:float = propertyMinimumFloat64
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["propertyDefaultFloat64", "propertyMaximumFloat64", "propertyMinimumFloat64"]
        values = [self.propertyDefaultFloat64, self.propertyMaximumFloat64, self.propertyMinimumFloat64]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)

class SubPropertyTemplateIdPropertiesInput(InputPart):
    def __init__(self, propertyDefaultId:str=None) -> None:
        super().__init__()
        self.propertyDefaultId:str = propertyDefaultId
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["propertyDefaultId"]
        values = [self.propertyDefaultId]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)

class SubPropertyTemplateInteger32PropertiesInput(InputPart):
    def __init__(self, propertyDefaultInteger32:int=None, propertyMaximumInteger32:int=None,
                 propertyMinimumInteger32:int=None) -> None:
        super().__init__()
        self.propertyDefaultInteger32:int = propertyDefaultInteger32
        self.propertyMaximumInteger32:int = propertyMaximumInteger32
        self.propertyMinimumInteger32:int = propertyMinimumInteger32
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["propertyDefaultInteger32", "propertyMaximumInteger32", "propertyMinimumInteger32"]
        values = [self.propertyDefaultInteger32, self.propertyMaximumInteger32, self.propertyMinimumInteger32]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)
    
class SubPropertyTemplateObjectPropertiesInput(InputPart):
    def __init__(self, allowsForeignObject:bool=False) -> None:
        super().__init__()
        self.allowsForeignObject=allowsForeignObject
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["allowsForeignObject"]
        values = [self.allowsForeignObject]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)


class PropertyTemplatePropertiesInput(InputPart):
    def __init__(self, cardinality:Cardinality=None, 
                 descriptiveTexts:LocalizedStringListInput=None, displayNames:LocalizedStringListInput=None, 
                 isHidden:bool=None, isNameProperty:bool=None, isValueRequired:bool=None,
                 modificationAccessRequired:int=None, settability:PropertySettability=None,
                 symbolicName:str=None, subPropertyTemplateBinaryProperties:SubPropertyTemplateBinaryPropertiesInput=None,
                 subPropertyTemplateBooleanProperties:SubPropertyTemplateBooleanPropertiesInput=None,
                 subPropertyTemplateDateTimeProperties:SubPropertyTemplateDateTimePropertiesInput=None,
                 subPropertyTemplateFloat64Properties:SubPropertyTemplateFloat64PropertiesInput=None,
                 subPropertyTemplateIdProperties:SubPropertyTemplateIdPropertiesInput=None,
                 subPropertyTemplateInteger32Properties:SubPropertyTemplateInteger32PropertiesInput=None,
                 subPropertyTemplateStringProperties:SubPropertyTemplateStringPropertiesInput=None,
                 subPropertyTemplateObjectProperties:SubPropertyTemplateObjectPropertiesInput=None,
                 choiceList:ObjectReferenceInput=None) -> None:
        super().__init__()
        self.cardinality:Cardinality = cardinality
        self.descriptiveTexts:LocalizedStringListInput = descriptiveTexts
        self.displayNames:LocalizedStringListInput = displayNames
        self.isHidden:bool = isHidden
        self.isNameProperty:bool = isNameProperty
        self.isValueRequired:bool = isValueRequired
        self.modificationAccessRequired:int = modificationAccessRequired
        self.settability:PropertySettability = settability
        self.symbolicName:str = symbolicName
        self.subPropertyTemplateBinaryProperties:SubPropertyTemplateBinaryPropertiesInput = subPropertyTemplateBinaryProperties
        self.subPropertyTemplateBooleanProperties:SubPropertyTemplateBooleanPropertiesInput = subPropertyTemplateBooleanProperties
        self.subPropertyTemplateDateTimeProperties:SubPropertyTemplateDateTimePropertiesInput = subPropertyTemplateDateTimeProperties
        self.subPropertyTemplateFloat64Properties:SubPropertyTemplateFloat64PropertiesInput = subPropertyTemplateFloat64Properties
        self.subPropertyTemplateIdProperties:SubPropertyTemplateIdPropertiesInput = subPropertyTemplateIdProperties
        self.subPropertyTemplateInteger32Properties:SubPropertyTemplateInteger32PropertiesInput = subPropertyTemplateInteger32Properties
        self.subPropertyTemplateStringProperties:SubPropertyTemplateStringPropertiesInput = subPropertyTemplateStringProperties
        self.subPropertyTemplateObjectProperties:SubPropertyTemplateObjectPropertiesInput = subPropertyTemplateObjectProperties
        self.choiceList=choiceList
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["cardinality", "descriptiveTexts", "displayNames", "isHidden",
                 "isNameProperty", "isValueRequired", "modificationAccessRequired", "settability",
                 "symbolicName", "subPropertyTemplateBinaryProperties", "subPropertyTemplateBooleanProperties", "subPropertyTemplateDateTimeProperties",
                 "subPropertyTemplateFloat64Properties", "subPropertyTemplateIdProperties", "subPropertyTemplateInteger32Properties", 
                 "subPropertyTemplateStringProperties", "choiceList"]
        values = [self.cardinality, self.descriptiveTexts, self.displayNames, self.isHidden,
                  self.isNameProperty, self.isValueRequired, self.modificationAccessRequired, self.settability,
                  self.symbolicName, self.subPropertyTemplateBinaryProperties, self.subPropertyTemplateBooleanProperties, self.subPropertyTemplateDateTimeProperties,
                  self.subPropertyTemplateFloat64Properties, self.subPropertyTemplateIdProperties, 
                  self.subPropertyTemplateInteger32Properties, self.subPropertyTemplateStringProperties, 
                  self.choiceList]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)

class SubPropertyDefinitionBinaryInput(InputPart):
    def __init__(self, maximumLengthBinary:int=None, propertyDefaultBinary:str=None) -> None:
        super().__init__()
        self.maximumLengthBinary:int = maximumLengthBinary
        self.propertyDefaultBinary:str = propertyDefaultBinary
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["maximumLengthBinary", "propertyDefaultBinary"]
        values = [self.maximumLengthBinary, self.propertyDefaultBinary]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)

class SubPropertyDefinitionBooleanInput(InputPart):
    def __init__(self, propertyDefaultBoolean:bool=None) -> None:
        super().__init__()
        self.propertyDefaultBoolean:bool = propertyDefaultBoolean
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["propertyDefaultBoolean"]
        values = [self.propertyDefaultBoolean]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)

class SubPropertyDefinitionDateTimeInput(InputPart):
    def __init__(self, isDateOnly:bool=None, propertyDefaultDateTime:str=None, 
                 propertyMaximumDateTime:str=None, propertyMinimumDateTime:str=None) -> None:
        super().__init__()
        self.isDateOnly:bool = isDateOnly
        self.propertyDefaultDateTime:str = propertyDefaultDateTime
        self.propertyMaximumDateTime:str = propertyMaximumDateTime
        self.propertyMinimumDateTime:str = propertyMinimumDateTime
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["isDateOnly", "propertyDefaultDateTime", "propertyMaximumDateTime", "propertyMinimumDateTime"]
        values = [self.isDateOnly, self.propertyDefaultDateTime, self.propertyMaximumDateTime, self.propertyMinimumDateTime]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)

class SubPropertyDefinitionFloat64Input(InputPart):
    def __init__(self, propertyDefaultFloat64:float=None, propertyMaximumFloat64:float=None, 
                 propertyMinimumFloat64:float=None) -> None:
        super().__init__()
        self.propertyDefaultFloat64:float = propertyDefaultFloat64
        self.propertyMaximumFloat64:float = propertyMaximumFloat64
        self.propertyMinimumFloat64:float = propertyMinimumFloat64
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["propertyDefaultFloat64", "propertyMaximumFloat64", "propertyMinimumFloat64"]
        values = [self.propertyDefaultFloat64, self.propertyMaximumFloat64, self.propertyMinimumFloat64]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)

class SubPropertyDefinitionIdInput(InputPart):
    def __init__(self, propertyDefaultId:str=None) -> None:
        super().__init__()
        self.propertyDefaultId:str = propertyDefaultId
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["propertyDefaultId"]
        values = [self.propertyDefaultId]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)

class SubPropertyDefinitionInteger32Input(InputPart):
    def __init__(self, propertyDefaultInteger32:int=None, propertyMaximumInteger32:int=None, 
                 propertyMinimumInteger32:int=None) -> None:
        super().__init__()
        self.propertyDefaultInteger32:int = propertyDefaultInteger32
        self.propertyMaximumInteger32:int = propertyMaximumInteger32
        self.propertyMinimumInteger32:int = propertyMinimumInteger32
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["propertyDefaultInteger32", "propertyMaximumInteger32", "propertyMinimumInteger32"]
        values = [self.propertyDefaultInteger32, self.propertyMaximumInteger32, self.propertyMinimumInteger32]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)

class SubPropertyDefinitionStringInput(InputPart):
    def __init__(self, maximumLengthString:int=None, propertyDefaultString:str=None) -> None:
        super().__init__()
        self.maximumLengthString:int = maximumLengthString
        self.propertyDefaultString:str = propertyDefaultString
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["maximumLengthString", "propertyDefaultString"]
        values = [self.maximumLengthString, self.propertyDefaultString]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)
    
class SubPropertyDefinitionObjectInput(InputPart):
    def __init__(self, requiredClassId:str=None, reflectivePropertyId:str=None) -> None:
        super().__init__()
        self.requiredClassId:str = requiredClassId
        self.reflectivePropertyId:str = reflectivePropertyId
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["requiredClassId", "reflectivePropertyId"]
        values = [self.requiredClassId, self.reflectivePropertyId]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)
    




class PropertyDefinitionInput(BaseDependentObjectInput):
    def __init__(self, insertAction:InsertDependentActionInput=None, updateAction:UpdateDependentActionInput=None,
                 moveAction:MoveDependentActionInput=None, deleteAction:DeleteDependentActionInput=None,
                 propertyTemplate:ObjectReferenceInput=None, copyToReservation:bool=None,
                 isHidden:bool=None, isNameProperty:bool=None, isValueRequired:bool=None,
                 modificationAccessRequired:int=None, settability:PropertySettability=None,
                 subPropertyDefinitionBinary:SubPropertyDefinitionBinaryInput=None, subPropertyDefinitionBoolean:SubPropertyDefinitionBooleanInput=None,
                 subPropertyDefinitionDateTime:SubPropertyDefinitionDateTimeInput=None, subPropertyDefinitionFloat64:SubPropertyDefinitionFloat64Input=None,
                 subPropertyDefinitionId:SubPropertyDefinitionIdInput=None, subPropertyDefinitionInteger32:SubPropertyDefinitionInteger32Input=None,
                 subPropertyDefinitionString:SubPropertyDefinitionStringInput=None,
                 subPropertyDefinitionObject:SubPropertyDefinitionObjectInput=None) -> None:
        super().__init__(insertAction=insertAction, updateAction=updateAction, moveAction=moveAction, deleteAction=deleteAction)
        self.propertyTemplate:ObjectReferenceInput = propertyTemplate
        self.copyToReservation:bool = copyToReservation
        self.isHidden:bool = isHidden
        self.isNameProperty:bool = isNameProperty
        self.isValueRequired:bool = isValueRequired
        self.modificationAccessRequired:int = modificationAccessRequired
        self.settability:PropertySettability = settability
        self.subPropertyDefinitionBinary:SubPropertyDefinitionBinaryInput = subPropertyDefinitionBinary
        self.subPropertyDefinitionBoolean:SubPropertyDefinitionBooleanInput = subPropertyDefinitionBoolean
        self.subPropertyDefinitionDateTime:SubPropertyDefinitionDateTimeInput = subPropertyDefinitionDateTime
        self.subPropertyDefinitionFloat64:SubPropertyDefinitionFloat64Input = subPropertyDefinitionFloat64
        self.subPropertyDefinitionId:SubPropertyDefinitionIdInput = subPropertyDefinitionId
        self.subPropertyDefinitionInteger32:SubPropertyDefinitionInteger32Input = subPropertyDefinitionInteger32
        self.subPropertyDefinitionString:SubPropertyDefinitionStringInput = subPropertyDefinitionString
        self.subPropertyDefinitionObject:SubPropertyDefinitionObjectInput = subPropertyDefinitionObject
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["propertyTemplate", "copyToReservation", "isHidden", "isNameProperty",
                 "isValueRequired", "modificationAccessRequired", "settability", "subPropertyDefinitionBinary",
                 "subPropertyDefinitionBoolean", "subPropertyDefinitionDateTime", "subPropertyDefinitionFloat64", "subPropertyDefinitionId",
                 "subPropertyDefinitionInteger32", "subPropertyDefinitionString", "subPropertyDefinitionObject"]
        values = [self.propertyTemplate, self.copyToReservation, self.isHidden, self.isNameProperty,
                  self.isValueRequired, self.modificationAccessRequired, self.settability, self.subPropertyDefinitionBinary,
                  self.subPropertyDefinitionBoolean, self.subPropertyDefinitionDateTime, self.subPropertyDefinitionFloat64, self.subPropertyDefinitionId,
                  self.subPropertyDefinitionInteger32, self.subPropertyDefinitionString,self.subPropertyDefinitionObject ]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)

class PropertyDefinitionListInput(InputPart):
    def __init__(self, modify:list[PropertyDefinitionInput]=None) -> None:
        super().__init__()
        self.modify:list[PropertyDefinitionInput] = modify
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["modify"]
        values = [self.modify]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)
    
class ClassDefinitionPropertiesInput(InputPart):
    def __init__(self, allowsInstances:bool=None, defaultInstanceOwner:str=None, defaultRetentionPeriod:int=None,
                 descriptiveTexts:LocalizedStringListInput=None, displayNames:LocalizedStringListInput=None,
                 isHidden:bool=None, owner:str=None, propertyDefinitions:PropertyDefinitionListInput=None,
                 retentionPeriodUnits:DurationUnits=None, symbolicName:str=None) -> None:
        super().__init__()
        self.allowsInstances:bool = allowsInstances
        self.defaultInstanceOwner:str = defaultInstanceOwner
        self.defaultRetentionPeriod:int = defaultRetentionPeriod
        self.descriptiveTexts:LocalizedStringListInput = descriptiveTexts
        self.displayNames:LocalizedStringListInput = displayNames
        self.isHidden:bool = isHidden
        self.owner:str = owner
        self.propertyDefinitions:PropertyDefinitionListInput = propertyDefinitions
        self.retentionPeriodUnits:DurationUnits = retentionPeriodUnits
        self.symbolicName:str = symbolicName
        # TODO: subSubscribableClassDefinitionProperties
    def to_graphql(self) -> str:
        strparts:list[str] = []
        strparts.append("{")
        strparts.append(super().to_graphql(fieldsOnly=True))
        names = ["allowsInstances", "defaultInstanceOwner", "defaultRetentionPeriod", "descriptiveTexts",
                 "displayNames", "isHidden", "owner", "propertyDefinitions",
                 "retentionPeriodUnits", "symbolicName"]
        values = [self.allowsInstances, self.defaultInstanceOwner, self.defaultRetentionPeriod, self.descriptiveTexts,
                  self.displayNames, self.isHidden, self.owner, self.propertyDefinitions,
                  self.retentionPeriodUnits, self.symbolicName]
        strparts.append(self._serializeFields(names, values))
        strparts.append(" }")
        return "".join(strparts)


