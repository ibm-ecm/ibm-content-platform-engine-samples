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
from enum import Enum, auto
from csdeploy.gqlschema.gqlcore import InlineFragment, OutputPart, OutputItem

class DurationUnits(Enum):
    DAYS = auto()
    HOURS = auto()
    MINUTES = auto()
    MONTHS = auto()
    SECONDS = auto()
    WEEKS = auto()
    YEARS = auto()

class ChoiceType(Enum):
    INTEGER = auto()
    MIDNODE_INTEGER = auto()
    MIDNODE_STRING = auto()
    STRING = auto()

class LocalizedStringType(OutputPart):
    def __init__(self) -> None:
        super().__init__()
    def field_id(self, alias=None) -> "LocalizedStringType":
        self.outputItems.append(OutputItem(fieldName="id", fieldAlias=alias))
        return self
    def field_localeName(self, alias=None) -> "LocalizedStringType":
        self.outputItems.append(OutputItem(fieldName="localeName", fieldAlias=alias))
        return self
    def field_localizedText(self, alias=None) -> "LocalizedStringType":
        self.outputItems.append(OutputItem(fieldName="localizedText", fieldAlias=alias))
        return self
class Choice(OutputPart):
    def __init__(self) -> None:
        super().__init__()
    def field_displayName(self, alias=None) -> "Choice":
        self.outputItems.append(OutputItem(fieldName="displayName", fieldAlias=alias))
        return self
    def field_displayNames(self, alias=None, fieldOutput:LocalizedStringType=None) -> "Choice":
        self.outputItems.append(OutputItem(fieldName="displayNames", fieldAlias=alias, fieldOutput=fieldOutput))
        return self
    def field_choiceType(self, alias=None) -> "Choice":
        self.outputItems.append(OutputItem(fieldName="choiceType", fieldAlias=alias))
        return self
    def field_choiceIntegerValue(self, alias=None) -> "Choice":
        self.outputItems.append(OutputItem(fieldName="choiceIntegerValue", fieldAlias=alias))
        return self
    def field_choiceStringValue(self, alias=None) -> "Choice":
        self.outputItems.append(OutputItem(fieldName="choiceStringValue", fieldAlias=alias))
        return self
    def field_choiceValues(self, alias=None, fieldOutput:"Choice"=None) -> "Choice":
        self.outputItems.append(OutputItem(fieldName="choiceValues", fieldAlias=alias, fieldOutput=fieldOutput))
        return self
    
class ChoiceList(OutputPart):
    def __init__(self) -> None:
        super().__init__()
    def field_creator(self, alias=None) -> "ChoiceList":
        self.outputItems.append(OutputItem(fieldName="creator", fieldAlias=alias))
        return self
    def field_dateCreated(self, alias=None) -> "ChoiceList":
        self.outputItems.append(OutputItem(fieldName="dateCreated", fieldAlias=alias))
        return self
    def field_lastModifier(self, alias=None) -> "ChoiceList":
        self.outputItems.append(OutputItem(fieldName="lastModifier", fieldAlias=alias))
        return self
    def field_dateLastModified(self, alias=None) -> "ChoiceList":
        self.outputItems.append(OutputItem(fieldName="dateLastModified", fieldAlias=alias))
        return self
    def field_id(self, alias=None) -> "ChoiceList":
        self.outputItems.append(OutputItem(fieldName="id", fieldAlias=alias))
        return self
    def field_name(self, alias=None) -> "ChoiceList":
        self.outputItems.append(OutputItem(fieldName="name", fieldAlias=alias))
        return self
    def field_owner(self, alias=None) -> "ChoiceList":
        self.outputItems.append(OutputItem(fieldName="owner", fieldAlias=alias))
        return self
    def field_dataType(self, alias=None) -> "ChoiceList":
        self.outputItems.append(OutputItem(fieldName="dataType", fieldAlias=alias))
        return self
    def field_choiceValues(self, alias=None, fieldOutput:Choice=None) -> "ChoiceList":
        self.outputItems.append(OutputItem(fieldName="choiceValues", fieldAlias=alias, fieldOutput=fieldOutput))
        return self
    def field_hasHierarchy(self, alias=None) -> "ChoiceList":
        self.outputItems.append(OutputItem(fieldName="hasHierarchy", fieldAlias=alias))
        return self
    def field_displayName(self, alias=None) -> "ChoiceList":
        self.outputItems.append(OutputItem(fieldName="displayName", fieldAlias=alias))
        return self
    def field_descriptiveText(self, alias=None) -> "ChoiceList":
        self.outputItems.append(OutputItem(fieldName="descriptiveText", fieldAlias=alias))
        return self
    
class PropertyTemplate(OutputPart):
    def __init__(self) -> None:
        super().__init__()
    def field_cardinality(self, alias=None) -> "PropertyTemplate":
        self.outputItems.append(OutputItem(fieldName="cardinality", fieldAlias=alias))
        return self
    def field_creator(self, alias=None) -> "PropertyTemplate":
        self.outputItems.append(OutputItem(fieldName="creator", fieldAlias=alias))
        return self
    def field_dataType(self, alias=None) -> "PropertyTemplate":
        self.outputItems.append(OutputItem(fieldName="dataType", fieldAlias=alias))
        return self
    def field_dateCreated(self, alias=None) -> "PropertyTemplate":
        self.outputItems.append(OutputItem(fieldName="dateCreated", fieldAlias=alias))
        return self
    def field_dateLastModified(self, alias=None) -> "PropertyTemplate":
        self.outputItems.append(OutputItem(fieldName="dateLastModified", fieldAlias=alias))
        return self
    def field_descriptiveTexts(self, alias=None, fieldOutput:LocalizedStringType=None) -> "PropertyTemplate":
        self.outputItems.append(OutputItem(fieldName="descriptiveTexts", fieldAlias=alias, fieldOutput=fieldOutput))
        return self
    def field_displayNames(self, alias=None, fieldOutput:LocalizedStringType=None) -> "PropertyTemplate":
        self.outputItems.append(OutputItem(fieldName="displayNames", fieldAlias=alias, fieldOutput=fieldOutput))
        return self
    def field_id(self, alias=None) -> "PropertyTemplate":
        self.outputItems.append(OutputItem(fieldName="id", fieldAlias=alias))
        return self
    def field_isHidden(self, alias=None) -> "PropertyTemplate":
        self.outputItems.append(OutputItem(fieldName="isHidden", fieldAlias=alias))
        return self
    def field_isNameProperty(self, alias=None) -> "PropertyTemplate":
        self.outputItems.append(OutputItem(fieldName="isNameProperty", fieldAlias=alias))
        return self
    def field_isValueRequired(self, alias=None) -> "PropertyTemplate":
        self.outputItems.append(OutputItem(fieldName="isValueRequired", fieldAlias=alias))
        return self
    def field_lastModifier(self, alias=None) -> "PropertyTemplate":
        self.outputItems.append(OutputItem(fieldName="lastModifier", fieldAlias=alias))
        return self
    def field_modificationAccessRequired(self, alias=None) -> "PropertyTemplate":
        self.outputItems.append(OutputItem(fieldName="modificationAccessRequired", fieldAlias=alias))
        return self
    def field_name(self, alias=None) -> "PropertyTemplate":
        self.outputItems.append(OutputItem(fieldName="name", fieldAlias=alias))
        return self
    def field_owner(self, alias=None) -> "PropertyTemplate":
        self.outputItems.append(OutputItem(fieldName="owner", fieldAlias=alias))
        return self
    def field_settability(self, alias=None) -> "PropertyTemplate":
        self.outputItems.append(OutputItem(fieldName="settability", fieldAlias=alias))
        return self
    def field_symbolicName(self, alias=None) -> "PropertyTemplate":
        self.outputItems.append(OutputItem(fieldName="symbolicName", fieldAlias=alias))
        return self
    def field_choiceList(self, alias=None, fieldOutput:ChoiceList=None) -> "PropertyTemplate":
        self.outputItems.append(OutputItem(fieldName="choiceList", fieldAlias=alias, fieldOutput=fieldOutput))
        return self

class PropertyDefinition(OutputPart):
    def __init__(self) -> None:
        super().__init__()
    def field_cardinality(self, alias=None) -> "PropertyDefinition":
        self.outputItems.append(OutputItem(fieldName="cardinality", fieldAlias=alias))
        return self
    def field_copyToReservation(self, alias=None) -> "PropertyDefinition":
        self.outputItems.append(OutputItem(fieldName="copyToReservation", fieldAlias=alias))
        return self
    def field_dataType(self, alias=None) -> "PropertyDefinition":
        self.outputItems.append(OutputItem(fieldName="dataType", fieldAlias=alias))
        return self
    def field_descriptiveText(self, alias=None) -> "PropertyDefinition":
        self.outputItems.append(OutputItem(fieldName="descriptiveText", fieldAlias=alias))
        return self
    def field_displayName(self, alias=None) -> "PropertyDefinition":
        self.outputItems.append(OutputItem(fieldName="displayName", fieldAlias=alias))
        return self
    def field_id(self, alias=None) -> "PropertyDefinition":
        self.outputItems.append(OutputItem(fieldName="id", fieldAlias=alias))
        return self
    def field_isHidden(self, alias=None) -> "PropertyDefinition":
        self.outputItems.append(OutputItem(fieldName="isHidden", fieldAlias=alias))
        return self
    def field_isNameProperty(self, alias=None) -> "PropertyDefinition":
        self.outputItems.append(OutputItem(fieldName="isNameProperty", fieldAlias=alias))
        return self
    def field_isSystemOwned(self, alias=None) -> "PropertyDefinition":
        self.outputItems.append(OutputItem(fieldName="isSystemOwned", fieldAlias=alias))
        return self
    def field_isValueRequired(self, alias=None) -> "PropertyDefinition":
        self.outputItems.append(OutputItem(fieldName="isValueRequired", fieldAlias=alias))
        return self
    def field_modificationAccessRequired(self, alias=None) -> "PropertyDefinition":
        self.outputItems.append(OutputItem(fieldName="modificationAccessRequired", fieldAlias=alias))
        return self
    def field_name(self, alias=None) -> "PropertyDefinition":
        self.outputItems.append(OutputItem(fieldName="name", fieldAlias=alias))
        return self
    def field_primaryId(self, alias=None) -> "PropertyDefinition":
        self.outputItems.append(OutputItem(fieldName="primaryId", fieldAlias=alias))
        return self
    def field_propertyTemplate(self, alias=None, fieldOutput:PropertyTemplate=None) -> "PropertyDefinition":
        self.outputItems.append(OutputItem(fieldName="propertyTemplate", fieldAlias=alias, fieldOutput=fieldOutput))
        return self
    def field_requiresUniqueElements(self, alias=None) -> "PropertyDefinition":
        self.outputItems.append(OutputItem(fieldName="requiresUniqueElements", fieldAlias=alias))
        return self
    def field_settability(self, alias=None) -> "PropertyDefinition":
        self.outputItems.append(OutputItem(fieldName="settability", fieldAlias=alias))
        return self
    def field_symbolicName(self, alias=None) -> "PropertyDefinition":
        self.outputItems.append(OutputItem(fieldName="symbolicName", fieldAlias=alias))
        return self
    def field_choiceList(self, alias=None, fieldOutput:ChoiceList=None) -> "PropertyDefinition":
        self.outputItems.append(OutputItem(fieldName="choiceList", fieldAlias=alias, fieldOutput=fieldOutput))
        return self
class ClassDefinition(OutputPart):
    def __init__(self) -> None:
        super().__init__()
    def field_id(self, alias=None) -> "ClassDefinition":
        self.outputItems.append(OutputItem(fieldName="id", fieldAlias=alias))
        return self
    def field_symbolicName(self, alias=None) -> "ClassDefinition":
        self.outputItems.append(OutputItem(fieldName="symbolicName", fieldAlias=alias))
        return self
    def field_allowsInstances(self, alias=None) -> "ClassDefinition":
        self.outputItems.append(OutputItem(fieldName="allowsInstances", fieldAlias=alias))
        return self
    def field_allowsPropertyAdditions(self, alias=None) -> "ClassDefinition":
        self.outputItems.append(OutputItem(fieldName="allowsPropertyAdditions", fieldAlias=alias))
        return self
    def field_allowsSubclasses(self, alias=None) -> "ClassDefinition":
        self.outputItems.append(OutputItem(fieldName="allowsSubclasses", fieldAlias=alias))
        return self
    def field_creator(self, alias=None) -> "ClassDefinition":
        self.outputItems.append(OutputItem(fieldName="creator", fieldAlias=alias))
        return self
    def field_dateCreated(self, alias=None) -> "ClassDefinition":
        self.outputItems.append(OutputItem(fieldName="dateCreated", fieldAlias=alias))
        return self
    def field_dateLastModified(self, alias=None) -> "ClassDefinition":
        self.outputItems.append(OutputItem(fieldName="dateLastModified", fieldAlias=alias))
        return self
    def field_defaultInstanceOwner(self, alias=None) -> "ClassDefinition":
        self.outputItems.append(OutputItem(fieldName="defaultInstanceOwner", fieldAlias=alias))
        return self
    def field_defaultRetentionPeriod(self, alias=None) -> "ClassDefinition":
        self.outputItems.append(OutputItem(fieldName="defaultRetentionPeriod", fieldAlias=alias))
        return self
    def field_descriptiveTexts(self, alias=None, fieldOutput:LocalizedStringType=None) -> "ClassDefinition":
        self.outputItems.append(OutputItem(fieldName="descriptiveTexts", fieldAlias=alias, fieldOutput=fieldOutput))
        return self
    def field_displayNames(self, alias=None, fieldOutput:LocalizedStringType=None) -> "ClassDefinition":
        self.outputItems.append(OutputItem(fieldName="displayNames", fieldAlias=alias, fieldOutput=fieldOutput))
        return self
    def field_isHidden(self, alias=None) -> "ClassDefinition":
        self.outputItems.append(OutputItem(fieldName="isHidden", fieldAlias=alias))
        return self
    def field_isSystemOwned(self, alias=None) -> "ClassDefinition":
        self.outputItems.append(OutputItem(fieldName="isSystemOwned", fieldAlias=alias))
        return self
    def field_lastModifier(self, alias=None) -> "ClassDefinition":
        self.outputItems.append(OutputItem(fieldName="lastModifier", fieldAlias=alias))
        return self
    def field_name(self, alias=None) -> "ClassDefinition":
        self.outputItems.append(OutputItem(fieldName="name", fieldAlias=alias))
        return self
    def field_owner(self, alias=None) -> "ClassDefinition":
        self.outputItems.append(OutputItem(fieldName="owner", fieldAlias=alias))
        return self
    def field_propertyDefinitions(self, alias=None, fieldOutput:PropertyDefinition=None) -> "ClassDefinition":
        self.outputItems.append(OutputItem(fieldName="propertyDefinitions", fieldAlias=alias, fieldOutput=fieldOutput))
        return self
    def field_protectedPropertyCount(self, alias=None) -> "ClassDefinition":
        self.outputItems.append(OutputItem(fieldName="protectedPropertyCount", fieldAlias=alias))
        return self
    def field_retentionPeriodUnits(self, alias=None) -> "ClassDefinition":
        self.outputItems.append(OutputItem(fieldName="retentionPeriodUnits", fieldAlias=alias))
        return self
    def field_superClassDefinition(self, alias=None, fieldOutput:'ClassDefinition'=None) -> "ClassDefinition":
        self.outputItems.append(OutputItem(fieldName="superClassDefinition", fieldAlias=alias, fieldOutput=fieldOutput))
        return self


    