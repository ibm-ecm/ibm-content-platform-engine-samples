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

"""Module contain classes necessary for deployment package object with information for import and export"""
import json

class ClassDefinitionSelection:
    """Class defining selected class definition
    """
    def __init__(self, id:str=None, symbolic_name:str=None, label:str=None) -> None:
        self.id = id
        self.symbolic_name = symbolic_name
        self.label = label
    def to_json(self) -> dict:
        """Converts query to json object
        Returns:
            dict: json object with information init
        """
        return {'id': self.id, 'symbolicName':self.symbolic_name, 'label':self.label}
    def from_json(self, json_object:dict) -> None:
        """converts from json to query
        Args:
            json_object (dict): json dict to convert to query object
        """
        self.id = json_object['id'] if 'id' in json_object else None
        self.symbolic_name = json_object['symbolicName'] if 'symbolicName' in json_object else None
        self.label = json_object['label'] if 'label' in json_object else None

class ExportSelection:
    """ Class containing list of selected class definition that is being exported
    """
    def __init__(self, class_definitions:list[ClassDefinitionSelection]=None) -> bool:
        self.class_definitions = class_definitions if class_definitions is not None else []
    def to_json(self) -> dict:
        """Converts query to json object
        Returns:
            dict: json object with information init
        """
        class_definitions = [cd_selection.to_json() for cd_selection in self.class_definitions]
        json_object = {
            'classDefinitions': class_definitions
        }
        return json_object
    def from_json(self, json_object:dict) -> None:
        """converts from json to query
        Args:
            json_object (dict): json dict to convert to query object
        """
        cd_selections = []
        if 'classDefinitions' in json_object and json_object['classDefinitions'] is not None:
            for cd_obj in json_object['classDefinitions']:
                cd_selection = ClassDefinitionSelection()
                cd_selection.from_json(cd_obj)
                cd_selections.append(cd_selection)
        self.class_definitions = cd_selections

class ExportQuery:
    """Class defining query to export necessary class defs, prop template, CL, and other objects
    """
    def __init__(self, retrievals:list[str]=None, query:str=None) -> None:
        self.retrievals=retrievals if retrievals is not None else []
        self.query=query
    def to_json(self) -> dict:
        """Converts query to json object
        Returns:
            dict: json object with information init
        """
        json_object = {
            'retrievals':self.retrievals,
            'query':self.query
        }
        return json_object
    def from_json(self, json_object:dict) -> None:
        """converts from json to query
        Args:
            json_object (dict): json dict to convert to query object
        """
        self.retrievals = json_object['retrievals'] if 'retrievals' in json_object else []
        self.query = json_object['query'] if 'query' in json_object else None

class DeploymentDependencies:
    """Class defining dependency between PT, CLs, CDs, and other objects
    """
    def __init__(self, property_templates:list[str]=None, choice_lists:list[str]=None, 
                 super_class_definition:str=None, object_prop_required_cds:list[str]=None) -> None:
        self.property_templates = property_templates if property_templates is not None else []
        self.choice_lists = choice_lists if choice_lists is not None else []
        self.super_class_definition = super_class_definition
        self.object_prop_required_cds = object_prop_required_cds if object_prop_required_cds is not None else []
    def to_json(self) -> dict:
        """Converts query to json object
        Returns:
            dict: json object with information init
        """
        json_object = {
            'propertyTemplates':self.property_templates,
            'choiceLists':self.choice_lists,
            'superClassDefinition':self.super_class_definition,
            'objectPropertyRequiredClassDefinitions':self.object_prop_required_cds
        }   
        return json_object
    def from_json(self, json_object:dict) -> None:
        """converts from json to query
        Args:
            json_object (dict): json dict to convert to query object
        """
        self.property_templates = json_object['propertyTemplates'] if 'propertyTemplates' in json_object else []
        self.choice_lists = json_object['choiceLists'] if 'choiceLists' in json_object else []
        self.super_class_definition = json_object['superClassDefinition'] if 'superClassDefinition' in json_object else None
        self.object_prop_required_cds = json_object['objectPropertyRequiredClassDefinitions'] if 'objectPropertyRequiredClassDefinitions' in json_object else []

class ClassDefinitionPlan:
    """Class defining plan to export CD
    """
    def __init__(self, reference_id:str=None, id:str=None, symbolic_name:str=None,
                 dependencies:DeploymentDependencies=None, starting_pd_idx:int=None,
                 export_data:dict=None) -> None:
        self.reference_id=reference_id
        self.id = id
        self.symbolic_name=symbolic_name
        self.dependencies=dependencies
        self.starting_pd_idx=starting_pd_idx
        self.export_data=export_data
    def to_json(self) -> dict:
        """Converts query to json object
        Returns:
            dict: json object with information init
        """
        json_object = {
            'referenceId':self.reference_id,
            'id':self.id,
            'symbolicName':self.symbolic_name,
            'dependencies':self.dependencies.to_json() if self.dependencies is not None else None,
            'startingPropertyDefinitionExportedIndex':self.starting_pd_idx,
            'exportData':self.export_data
        }
        return json_object
    def from_json(self, json_object:dict) -> None:
        """converts from json to query
        Args:
            json_object (dict): json dict to convert to query object
        """
        self.reference_id = json_object['referenceId'] if 'referenceId' in json_object else None
        self.id = json_object['id'] if 'id' in json_object else None
        self.symbolic_name = json_object['symbolicName'] if 'symbolicName' in json_object else None
        deps = None
        if 'dependencies' in json_object and json_object['dependencies'] is not None:
            deps = DeploymentDependencies()
            deps.from_json(json_object['dependencies'])
        self.dependencies = deps
        self.starting_pd_idx = json_object['startingPropertyDefinitionExportedIndex'] if 'startingPropertyDefinitionExportedIndex' in json_object else None
        self.export_data = json_object['exportData'] if 'exportData' in json_object else None

class ChoiceListPlan:
    """Class defining plan to export CL
    """
    def __init__(self, reference_id:str=None, id:str=None, display_name:str=None,
                 dependencies:DeploymentDependencies=None, export_data:dict=None) -> None:
        self.reference_id=reference_id
        self.id = id
        self.display_name=display_name
        self.dependencies=dependencies
        self.export_data=export_data
    def to_json(self) -> dict:
        """Converts query to json object
        Returns:
            dict: json object with information init
        """
        json_object = {
            'referenceId':self.reference_id,
            'id':self.id,
            'displayName':self.display_name,
            'dependencies':self.dependencies.to_json() if self.dependencies is not None else None,
            
            'exportData':self.export_data
        }
        return json_object
    def from_json(self, json_object:dict) -> None:
        """converts from json to query
        Args:
            json_object (dict): json dict to convert to query object
        """
        self.reference_id = json_object['referenceId'] if 'referenceId' in json_object else None
        self.id = json_object['id'] if 'id' in json_object else None
        self.symbolic_name = json_object['displayName'] if 'displayName' in json_object else None
        deps = None
        if 'dependencies' in json_object and json_object['dependencies'] is not None:
            deps = DeploymentDependencies()
            deps.from_json(json_object['dependencies'])
        self.dependencies = deps        
        self.export_data = json_object['exportData'] if 'exportData' in json_object else None

class PropertyTemplatePlan:
    """Class defining plan to export PT"""
    def __init__(self, reference_id:str=None, id:str=None, symbolic_name:str=None,
                 dependencies:DeploymentDependencies=None, export_data:dict=None) -> None:
        self.reference_id=reference_id
        self.id = id
        self.symbolic_name=symbolic_name
        self.dependencies=dependencies
        self.export_data=export_data
    def to_json(self) -> dict:
        """Converts query to json object
        Returns:
            dict: json object with information init
        """
        json_object = {
            'referenceId':self.reference_id,
            'id':self.id,
            'symbolicName':self.symbolic_name,
            'dependencies':self.dependencies.to_json() if self.dependencies is not None else None,
            'exportData':self.export_data
        }
        return json_object
    def from_json(self, json_object:dict) -> None:
        """converts from json to query
        Args:
            json_object (dict): json dict to convert to query object
        """
        self.reference_id = json_object['referenceId'] if 'referenceId' in json_object else None
        self.id = json_object['id'] if 'id' in json_object else None
        self.symbolic_name = json_object['symbolicName'] if 'symbolicName' in json_object else None
        deps = None
        if 'dependencies' in json_object and json_object['dependencies'] is not None:
            deps = DeploymentDependencies()
            deps.from_json(json_object['dependencies'])
        self.dependencies = deps
        self.export_data = json_object['exportData'] if 'exportData' in json_object else None

class DeploymentPlan:
    """Plan for deployment of CD, PT, and CL"""
    def __init__(self, class_definitions:list[ClassDefinitionPlan]=None, 
                 property_templates:list[PropertyTemplatePlan]=None,
                 choice_lists:list[ChoiceListPlan]=None) -> None:
        self.class_definitions = class_definitions if class_definitions is not None else []
        self.property_templates = property_templates if property_templates is not None else []
        self.choice_lists = choice_lists if choice_lists is not None else []
    def to_json(self) -> dict:
        """Converts query to json object
        Returns:
            dict: json object with information init
        """
        json_object = {
            'classDefinitions':[cd_plan.to_json() for cd_plan in self.class_definitions],
            'propertyTemplates':[pt_plan.to_json() for pt_plan in self.property_templates],
            'choiceLists':[cvl_plan.to_json() for cvl_plan in self.choice_lists]
        }
        return json_object
    def from_json(self, json_object:dict) -> None:
        """converts from json to query
        Args:
            json_object (dict): json dict to convert to query object
        """
        class_definitions = []
        if 'classDefinitions' in json_object and json_object['classDefinitions'] is not None:
            for cd_obj in json_object['classDefinitions']:
                cd_plan = ClassDefinitionPlan()
                cd_plan.from_json(cd_obj)
                class_definitions.append(cd_plan)
        self.class_definitions = class_definitions
        property_templates = []
        if 'propertyTemplates' in json_object and json_object['propertyTemplates'] is not None:
            for pt_obj in json_object['propertyTemplates']:
                pt_plan = PropertyTemplatePlan()
                pt_plan.from_json(pt_obj)
                property_templates.append(pt_plan)
        self.property_templates = property_templates
        choice_lists = []
        if 'choiceLists' in json_object and json_object['choiceLists'] is not None:
            for cvlobj in json_object['choiceLists']:
                cvl_plan = ChoiceListPlan()
                cvl_plan.from_json(cvlobj)
                choice_lists.append(cvl_plan)
        self.choice_lists = choice_lists


class DeploymentPackage:
    """Package with all meta data on deploying selected class,
        modified by Exporter and used by Importer
    """
    def __init__(self, export_selection:ExportSelection=None, export_queries:list[ExportQuery]=None,
                 deployment_plan:DeploymentPlan=None) -> None:
        self.export_selection=export_selection
        self.export_queries=export_queries if export_queries is not None else []
        self.deployment_plan=deployment_plan

    def to_json(self) -> dict:
        """Converts query to json object
        Returns:
            dict: json object with information init
        """
        json_object = {
            'exportSelection':self.export_selection.to_json() if self.export_selection is not None else None,
            'exportQueries':[expq.to_json() for expq in self.export_queries],
            'deploymentPlan':self.deployment_plan.to_json() if self.deployment_plan is not None else None,
        }
        return json_object
    def from_json(self, json_object:dict) -> None:
        """converts from json to query
        Args:
            json_object (dict): json dict to convert to query object
        """
        export_selection = None
        if 'exportSelection' in json_object and json_object['exportSelection'] is not None:
            export_selection = ExportSelection()
            export_selection.from_json(json_object['exportSelection'])
        self.export_selection = export_selection
        export_queries = []
        if 'exportQueries' in json_object and json_object['exportQueries'] is not None:
            for expqryobj in json_object['exportQueries']:
                export_query = ExportQuery()
                export_query.from_json(expqryobj)
                export_queries.append(export_query)
        self.export_queries = export_queries
        deployment_plan = None
        if 'deploymentPlan' in json_object and json_object['deploymentPlan'] is not None:
            deployment_plan = DeploymentPlan()
            deployment_plan.from_json(json_object['deploymentPlan'])
        self.deployment_plan = deployment_plan
    def write(self, ofile) -> None:
        """Write JSON file with deployment package information
        Args:
            ofile (_type_): file to write to
        """
        with open(ofile, "w") as output:
            json_obj = self.to_json()
            json.dump(json_obj, output, indent=4)
    def read(self, rfile) -> None:
        """Read package from file
        Args:
            rfile (_type_): file to read from
        """
        json_obj = json.load(open(rfile, "r"))
        self.from_json(json_obj)

    def get_obj_requiring_export_data(self) -> set:
        """Get all objects requiring export data

        Returns:
            set: set containing all required objects
        """
        req_objs = set()
        for cd_plan in self.deployment_plan.class_definitions:
            if not cd_plan.export_data:
                req_objs.add(cd_plan.reference_id)
        for pt_plan in self.deployment_plan.property_templates:
            if not pt_plan.export_data:
                req_objs.add(pt_plan.reference_id)
        for cvl_plan in self.deployment_plan.choice_lists:
            if not cvl_plan.export_data:
                req_objs.add(cvl_plan.reference_id)
        return req_objs

    def get_deployment_obj_maps(self) -> tuple:
        """Gets map of PT, CD, CLs plans

        Returns:
            tuple: map of objects sorted by reference id and map of objects sorted by id
        """
        ref_deployed_obj = {}
        pt_id = {}
        cvl_id = {}
        cd_id = {}
        id_deployed_obj = {}
        id_deployed_obj['propertyTemplates'] = pt_id
        id_deployed_obj['classDefinitions'] = cd_id
        id_deployed_obj['choiceLists'] = cvl_id
        for cd_plan in self.deployment_plan.class_definitions:
            ref_deployed_obj[cd_plan.reference_id] = cd_plan
            cd_id[cd_plan.id] = cd_plan
        for pt_plan in self.deployment_plan.property_templates:
            ref_deployed_obj[pt_plan.reference_id] = pt_plan
            pt_id[pt_plan.id] = pt_plan
        for cvl_plan in self.deployment_plan.choice_lists:
            ref_deployed_obj[cvl_plan.reference_id] = cvl_plan
            cvl_id[cvl_plan.id] = cvl_plan
        return ref_deployed_obj, id_deployed_obj

    def get_export_query_refs(self) -> set:
        """Get reference id of export query

        Returns:
            set: set containing reference ids
        """
        refs = set()
        for export_query in self.export_queries:
            for ref_id in export_query.retrievals:
                refs.add(ref_id)
        return refs
