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

""" Module containing Classes to Export and Import using GraphQL"""
from csdeploy.gqlinvoke import GraphqlConnection, GraphqlRequest
from csdeploy.gqlschema.admin import ChoiceInput, ChoiceListInput, ChoiceListPropertiesInput,\
    ChoiceType, ClassDefinitionPropertiesInput, InsertDependentActionInput, LocalizedStringInput,\
    LocalizedStringListInput, PropertyDefinitionBinary, PropertyDefinitionBoolean,\
    PropertyDefinitionDateTime, PropertyDefinitionFloat64, PropertyDefinitionId,\
    PropertyDefinitionInput, PropertyDefinitionInteger32, PropertyDefinitionListInput,\
    PropertyDefinitionObject, PropertyDefinitionString, PropertyTemplateBinary,\
    PropertyTemplateBoolean, PropertyTemplateDateTime, PropertyTemplateFloat64, PropertyTemplateId,\
    PropertyTemplateInteger32, PropertyTemplateObject, PropertyTemplatePropertiesInput,\
    PropertyTemplateString, SubPropertyDefinitionBinaryInput, SubPropertyDefinitionBooleanInput,\
    SubPropertyDefinitionDateTimeInput, SubPropertyDefinitionFloat64Input,\
    SubPropertyDefinitionIdInput, SubPropertyDefinitionInteger32Input,\
    SubPropertyDefinitionObjectInput, SubPropertyDefinitionStringInput,\
    SubPropertyTemplateBinaryPropertiesInput, SubPropertyTemplateBooleanPropertiesInput,\
    SubPropertyTemplateDateTimePropertiesInput, SubPropertyTemplateFloat64PropertiesInput,\
    SubPropertyTemplateIdPropertiesInput, SubPropertyTemplateInteger32PropertiesInput,\
    SubPropertyTemplateObjectPropertiesInput, \
SubPropertyTemplateStringPropertiesInput
from csdeploy.gqlschema.adminbase import Choice, ChoiceList, ClassDefinition, \
DurationUnits, LocalizedStringType, PropertyDefinition, PropertyTemplate
from csdeploy.gqlschema.corebase import ObjectReferenceInput
from csdeploy.gqlschema.coreinput import DependentItemReferenceInput, UpdateDependentActionInput
from csdeploy.gqlschema.gqlcore import NULL_VALUE, InlineFragment, OutputPart
from csdeploy.gqlschema.operation import Mutation, Query
from csdeploy.gqlschema.propertybase import Cardinality, PropertySettability, TypeID
from csdeploy.pkg import ChoiceListPlan, ClassDefinitionPlan, DeploymentDependencies, \
    DeploymentPlan, ExportQuery, ExportSelection, PropertyTemplatePlan
from csdeploy.pkg import DeploymentPackage


class Exporter:
    """ Class used to generate export info on selected item into deployment package
    """
    def __init__(self, gql_connection:GraphqlConnection, object_store_name:str,
                    package:DeploymentPackage, max_level_cvl:int=3) -> None:
        self.gql_connection = gql_connection
        self.object_store_name = object_store_name
        self.deployment_package = package
        self.max_level_cvl = max_level_cvl
        self.cvl_idx = 0
        self.pt_idx = 0
        self.cd_idx = 0

    def initialize_selection(self, selection:ExportSelection) -> None:
        """Initialize item to export into deployment package
        Args:
            selection (ExportSelection): ExportSelection object containing item to export
        """
        self.deployment_package.export_selection = selection
        self.deployment_package.export_queries = []
        self.deployment_package.deployment_plan = DeploymentPlan()
        self.deployment_package.import_discovery_queries = []
        self.deployment_package.import_mutations = []
        for cd_selection in self.deployment_package.export_selection.class_definitions:
            self.cd_idx += 1
            formatted_number = "{:03d}".format(self.cd_idx)
            rid = "cd" + formatted_number
            cd_plan = ClassDefinitionPlan(reference_id=rid, id=cd_selection.id,
                                                symbolic_name=cd_selection.symbolic_name)
            self.deployment_package.deployment_plan.class_definitions.append(cd_plan)

    def generate_queries(self) -> None:
        """ Generate necessary queries and add them into deployment package before execution
        """
        retrievals = []
        query = Query()
        export_query_refs = self.deployment_package.get_export_query_refs()
        for property_tempalte in self.deployment_package.deployment_plan.property_templates:
            if property_tempalte.reference_id not in export_query_refs:
                self._add_property_template_query(query, property_tempalte)
                retrievals.append(property_tempalte.reference_id)
        for class_definition in self.deployment_package.deployment_plan.class_definitions:
            if class_definition.reference_id not in export_query_refs:
                self._add_class_definition_query(query, class_definition)
                retrievals.append(class_definition.reference_id)
        for choice_list in self.deployment_package.deployment_plan.choice_lists:
            if choice_list.reference_id not in export_query_refs:
                self._add_choice_list_query(query, choice_list)
                retrievals.append(choice_list.reference_id)
        if len(query.outputItems) != 0:
            query_string = query.to_query()
            self.deployment_package.export_queries.append(ExportQuery(retrievals=retrievals, query=query_string))


    def export(self, auto_resolve_deps: bool = False) -> None:
        """Execute queries necessary to export info about selected item

        Args:
            auto_resolve_deps (bool, optional): Auto generate queries for dependency
                resolution of item. Defaults to False.
        """
        new_queries = True

        while new_queries:
            new_queries = False
            if auto_resolve_deps:
                self.generate_queries()
            objs_to_export = self.deployment_package.get_obj_requiring_export_data()
            ref_deployed_obj, id_deployed_obj = self.deployment_package.get_deployment_obj_maps()
            queries_queue = [False for i in range(len(self.deployment_package.export_queries))]
            for (idx,export_query) in enumerate(self.deployment_package.export_queries):
                for retrieval in export_query.retrievals:
                    if retrieval in objs_to_export:
                        # print("Executing query " + str(idx) + " to retrieve reference id " + retrieval)
                        queries_queue[idx] = True
                        new_queries = auto_resolve_deps
            for i in range(len(self.deployment_package.export_queries)):
                if not queries_queue[i]:
                    continue
                gql_req = GraphqlRequest(self.gql_connection)
                resp = gql_req.execute_request(self.deployment_package.export_queries[i].query)
                export_jsons = resp.json()['data']
                cl_deps = []

                if export_jsons is not None:
                    for rid,export_json in export_jsons.items():
                        #note that objsReqExp should have no spaces
                        if rid not in objs_to_export:
                            continue
                        if rid.startswith("cl"):
                            cvl_plan = ref_deployed_obj[rid]
                            deps = DeploymentDependencies()
                            cvl_plan.dependencies = deps
                            cvl_plan.export_data = export_json
                        elif rid.startswith("pt"):
                            pt_plan = ref_deployed_obj[rid]
                            deps = DeploymentDependencies()
                            pt_plan.dependencies = deps
                            pt_plan.export_data = export_json
                            choice_list = export_json['choiceList']
                            # check if this PT uses cvl
                            if choice_list is not None:
                                cl_deps.append(choice_list['id'])
                                deps = DeploymentDependencies(choice_lists=cl_deps)
                                pt_plan.dependencies = deps
                                if not choice_list['id'] in id_deployed_obj['choiceLists']:
                                    displayName = choice_list['displayName']
                                    self.cvl_idx += 1
                                    formatted_number = "{:03d}".format(self.cvl_idx)
                                    cvlrid = "cl" + formatted_number
                                    cvl_plan = ChoiceListPlan(reference_id=cvlrid, id=choice_list['id'], display_name=choice_list['displayName'])
                                    self.deployment_package.deployment_plan.choice_lists.append(cvl_plan)
                                    id_deployed_obj['choiceLists'][choice_list['id']] = cvl_plan

                        elif rid.startswith("cd"):
                            cd_plan = ref_deployed_obj[rid]
                            systemOwned = export_json['isSystemOwned']
                            if systemOwned is True:
                                data = {}
                                data['id'] = export_json['id']
                                data['symbolicName'] = export_json['symbolicName']
                                data['isSystemOwned'] = export_json['isSystemOwned']
                                data['displayNames'] = export_json['displayNames']
                                data['descriptiveTexts'] = export_json['descriptiveTexts']
                                data['propertyDefinitions'] = {} # for now, will change later to allow PDs
                                cd_plan.export_data=data
                                continue
                            start_pd_idx = export_json['protectedPropertyCount']
                            #print("Start property definition index: " + str(startpdidx))
                            export_json['propertyDefinitions'] = export_json['propertyDefinitions'][start_pd_idx:]
                            #print(json.dumps(expjson, indent=4))
                            #print(str([pdef['propertyTemplate']['id'] for pdef in expjson['propertyDefinitions']]))
                            #ptdeps = [pdef['propertyTemplate']['id'] for pdef in expjson['propertyDefinitions']]
                            pt_deps = []
                            obj_prop_req_cds = []
                            for property_definition in export_json['propertyDefinitions']:
                                if 'requiredClassId' in property_definition and property_definition['requiredClassId'] is not None:
                                    req_class_ids = property_definition['requiredClassId']
                                    self._need_add_clsdef(req_class_ids, None)
                                    obj_prop_req_cds.append(req_class_ids)
                                    #print("added "+reqClsId)
                                pt = property_definition['propertyTemplate']
                                pt_deps.append(pt['id'])
                                if not pt['id'] in id_deployed_obj['propertyTemplates']:
                                    #print("Property template missing from deployment data: " + pt['id'])
                                    self.pt_idx += 1
                                    formatted_number = "{:03d}".format(self.pt_idx)
                                    pt_rid = "pt" + formatted_number
                                    pt_plan = PropertyTemplatePlan(reference_id=pt_rid, id=pt['id'], symbolic_name=pt['symbolicName'])
                                    self.deployment_package.deployment_plan.property_templates.append(pt_plan)
                                    id_deployed_obj['propertyTemplates'][pt['id']] = pt_plan
                                choice_list = property_definition['choiceList']
                                if choice_list is not None:
                                    cl_deps.append(choice_list['id'])
                                    if not choice_list['id'] in id_deployed_obj['choiceLists']:
                                        displayName = choice_list['displayName']
                                        self.cvl_idx += 1
                                        formatted_number = "{:03d}".format(self.cvl_idx)
                                        cvlrid = "cl" + formatted_number
                                        cvl_plan = ChoiceListPlan(reference_id=cvlrid, id=choice_list['id'], display_name=choice_list['displayName'])
                                        self.deployment_package.deployment_plan.choice_lists.append(cvl_plan)
                                        id_deployed_obj['choiceLists'][choice_list['id']] = cvl_plan
                            super_class_definition = None
                            if export_json['superClassDefinition'] is not None:
                                super_class_definition = export_json['superClassDefinition']

                                self._need_add_clsdef(super_class_definition['id'], super_class_definition['symbolicName'])
                            deps = DeploymentDependencies(property_templates=pt_deps, choice_lists=cl_deps,
                                                          super_class_definition=super_class_definition,
                                                          object_prop_required_cds=obj_prop_req_cds)

                            cd_plan.dependencies=deps
                            cd_plan.starting_pd_idx=start_pd_idx
                            cd_plan.export_data=export_json
                        else:
                            print("Unexpected: encountered reference id of: " + rid)

    def _need_add_clsdef(self, id:str=None, symbolic_name:str=None) -> bool:
        """Add only class definitions that needs to be exported into deployment package
        Args:
            id (str, optional): id of targeted class def. Defaults to None.
            symbolic_name (str, optional): symbolic name of targeted class def. Defaults to None.

        Returns:
            bool: True if the class def is required and added, else false
        """
        existing_class = self.deployment_package.deployment_plan.class_definitions
        for cls in existing_class:
            existing_id = cls.id
            if id == existing_id:
                return False

        self.cd_idx += 1
        formatted_number = "{:03d}".format(self.cd_idx)
        ref_id = "cd" + formatted_number
        clsdefplan = ClassDefinitionPlan(reference_id=ref_id, id=id, symbolic_name=symbolic_name)
        self.deployment_package.deployment_plan.class_definitions.append(clsdefplan)
        #even though it is added to the plan, and we'll query it, but if it is a system class, we may not export it
        return True

    def _add_choice_list_query(self, qry:Query, plan:ChoiceListPlan) -> None:
        """Create query for choicelist export
        Args:
            qry (Query): Query to populate
            plan (ChoiceListPlan): Plan containing choicelist information
        """
        loc_string_out = LocalizedStringType().field_localeName().field_localizedText()
        cvl_out = ChoiceList()
        cvl_level_out = Choice() \
            .field_displayName() \
            .field_displayNames(fieldOutput=LocalizedStringType().field_localeName().field_localizedText()) \
            .field_choiceType() \
            .field_choiceIntegerValue() \
            .field_choiceStringValue()
        i = self.max_level_cvl
        while i > 1:
            cvl_level_out = Choice() \
            .field_displayName() \
            .field_displayNames(fieldOutput=LocalizedStringType().field_localeName().field_localizedText()) \
            .field_choiceType() \
            .field_choiceIntegerValue() \
            .field_choiceStringValue() \
            .field_choiceValues(fieldOutput=cvl_level_out)
            i=i-1


        cvl_out.field_id()\
                .field_displayName()\
                .field_descriptiveText()\
                .field_dataType()\
                .field_choiceValues("choiceValues", cvl_level_out)
        alias = plan.reference_id
        alias = alias.replace(" ", "")
        qry.field_choiceList(repositoryIdentifier=self.object_store_name,
                                      identifier=plan.id, alias=alias,
                                      fieldOutput=cvl_out)

    def _add_property_template_query(self, qry:Query, plan:PropertyTemplatePlan) -> None:
        """Create query for property template export

        Args:
            qry (Query): Query to populate
            plan (PropertyTemplatePlan): Plan containing property template information
        """
        loc_string_out = LocalizedStringType().field_localeName().field_localizedText()
        prop_template_out = PropertyTemplate()
        prop_template_out.field_id()\
                    .field_symbolicName()\
                    .field_displayNames(fieldOutput=loc_string_out)\
                    .field_descriptiveTexts(fieldOutput=loc_string_out)\
                    .field_dataType()\
                    .field_cardinality()\
                    .field_isHidden()\
                    .field_isNameProperty()\
                    .field_isValueRequired()\
                    .field_modificationAccessRequired()\
                    .field_settability()\
                    .field_choiceList(fieldOutput=ChoiceList().field_id().field_displayName()) \
                    .inlineFragment(frag=InlineFragment(onOutput=PropertyTemplateId().field_propertyDefaultId()))\
                    .inlineFragment(frag=InlineFragment(onOutput=PropertyTemplateBinary().field_propertyDefaultBinary().field_maximumLengthBinary()))\
                    .inlineFragment(frag=InlineFragment(onOutput=PropertyTemplateString().field_propertyDefaultString().field_maximumLengthString()))\
                    .inlineFragment(frag=InlineFragment(onOutput=PropertyTemplateBoolean().field_propertyDefaultBoolean()))\
                    .inlineFragment(frag=InlineFragment(onOutput=PropertyTemplateFloat64().field_propertyDefaultFloat64()\
                                                                                          .field_propertyMaximumFloat64()\
                                                                                          .field_propertyMinimumFloat64()))\
                    .inlineFragment(frag=InlineFragment(onOutput=PropertyTemplateDateTime().field_propertyDefaultDateTime()\
                                                                                           .field_propertyMaximumDateTime()\
                                                                                           .field_propertyMinimumDateTime()))\
                    .inlineFragment(frag=InlineFragment(onOutput=PropertyTemplateInteger32().field_propertyDefaultInteger32()\
                                                                                            .field_propertyMaximumInteger32()\
                                                                                            .field_propertyMinimumInteger32()))\
                    .inlineFragment(frag=InlineFragment(onOutput=PropertyTemplateObject()\
                                                                                            .field_allowsForeignObject()))

        qry.field_admPropertyTemplate(repositoryIdentifier=self.object_store_name,
                                      identifier=plan.id, alias=plan.reference_id,
                                      fieldOutput=prop_template_out)

    def _add_class_definition_query(self, qry:Query, plan:ClassDefinitionPlan) -> None:
        """Create  query for class definition export

        Args:
            qry (Query): Query to populate
            plan (ClassDefinitionPlan): Plan containing class definition information
        """
        prop_definition_out = PropertyDefinition()
        prop_definition_out.field_id()\
                  .field_name()\
                  .field_dataType()\
                  .field_cardinality()\
                  .field_copyToReservation()\
                  .field_isHidden()\
                  .field_isNameProperty()\
                  .field_isValueRequired()\
                  .field_modificationAccessRequired()\
                  .field_settability()\
                  .field_propertyTemplate(fieldOutput=PropertyTemplate().field_id().field_symbolicName())\
                  .inlineFragment(frag=InlineFragment(onOutput=PropertyDefinitionId().field_propertyDefaultId()))\
                  .inlineFragment(frag=InlineFragment(onOutput=PropertyDefinitionBinary().field_propertyDefaultBinary().field_maximumLengthBinary()))\
                  .inlineFragment(frag=InlineFragment(onOutput=PropertyDefinitionString().field_propertyDefaultString().field_maximumLengthString()))\
                  .inlineFragment(frag=InlineFragment(onOutput=PropertyDefinitionBoolean().field_propertyDefaultBoolean()))\
                  .inlineFragment(frag=InlineFragment(onOutput=PropertyDefinitionFloat64().field_propertyDefaultFloat64()\
                                                                                          .field_propertyMaximumFloat64()\
                                                                                          .field_propertyMinimumFloat64()))\
                  .inlineFragment(frag=InlineFragment(onOutput=PropertyDefinitionDateTime().field_propertyDefaultDateTime()\
                                                                                           .field_propertyMaximumDateTime()\
                                                                                           .field_propertyMinimumDateTime()))\
                  .inlineFragment(frag=InlineFragment(onOutput=PropertyDefinitionInteger32().field_propertyDefaultInteger32()\
                                                                                            .field_propertyMaximumInteger32()\
                                                                                            .field_propertyMinimumInteger32()))\
                  .inlineFragment(frag=InlineFragment(onOutput=PropertyDefinitionObject()\
                                                                                          .field_requiredClassId()\
                                                                                          .field_reflectivePropertyId()))\
                  .field_choiceList(fieldOutput=ChoiceList().field_id().field_displayName())

        loc_string_out = LocalizedStringType().field_localeName().field_localizedText()
        class_definition_out = ClassDefinition()
        class_definition_out.field_id()\
                 .field_symbolicName()\
                 .field("superClassDefinition", fieldOutput=OutputPart().field("symbolicName").field('id'))
        class_definition_out.field_displayNames(fieldOutput=loc_string_out)\
                 .field_descriptiveTexts(fieldOutput=loc_string_out)\
                 .field_defaultRetentionPeriod()\
                 .field_retentionPeriodUnits()\
                 .field_allowsInstances()\
                 .field_protectedPropertyCount()\
                 .field_propertyDefinitions(fieldOutput=prop_definition_out) \
                 .field_isSystemOwned()
        qry.field_admClassDefinition(repositoryIdentifier=self.object_store_name,
                                     identifier=plan.id, alias=plan.reference_id,
                                     fieldOutput=class_definition_out)

class ImportDiscoveryQuery:
    """Class for query to check for existing import
    """
    def __init__(self, retrievals:list[str]=None, query:str=None) -> None:
        self.retrievals=retrievals if retrievals is not None else []
        self.query=query
    def to_json(self) -> dict:
        """Converts query to JSON object
        Returns:
            dict: return json obj
        """
        #print("ImportDiscoveryQuery#to_json called. type retrievals=" + str(type(self.retrievals)) + "; type query=" + str(type(self.query)))
        jsonobj = {
            'retrievals':self.retrievals,
            'query':self.query
        }
        return jsonobj
    def from_json(self, jsonobj:dict) -> None:
        """Converts from JSON to query
        Args:
            jsonobj (dict): json dict to convert to query object
        """
        self.retrievals = jsonobj['retrievals'] if 'retrievals' in jsonobj else None
        self.query = jsonobj['query'] if 'query' in jsonobj else None


class ImportMutation:
    """Class representing an import mutation object
    """
    def __init__(self, modifications:list[str]=None, mutation:str=None, description:str=None) -> None:
        self.modifications=modifications if modifications is not None else []
        self.mutation=mutation
        self.description=description
    def to_json(self) -> dict:
        """Converts query to JSON object
        Returns:
            dict: return json obj
        """
        json_object = {
            'modifications':self.modifications,
            'mutation':self.mutation,
            'description':self.description
        }
        return json_object
    def from_json(self, jsonobj:dict) -> None:
        """Converts from JSON to query
        Args:
            jsonobj (dict): json dict to convert to query object
        """
        self.modifications = jsonobj['modifications'] if 'modifications' in jsonobj else None
        self.mutation = jsonobj['mutation'] if 'mutation' in jsonobj else None
        self.description = jsonobj['description'] if 'description' in jsonobj else None


class Importer:
    """Class for generating mutations based on deployment package
    """
    def __init__(self, gql_connection:GraphqlConnection, object_store_name:str, deployment_package:DeploymentPackage,
                discovery_queries:list[ImportDiscoveryQuery]=None, import_mutations:list[ImportMutation]=None) -> None:
        self.gql_connection = gql_connection
        self.object_store_name = object_store_name
        self.deployment_package = deployment_package
        self.discovery_queries = discovery_queries if discovery_queries is not None else []
        self.import_mutations = import_mutations if import_mutations is not None else []

    def to_json(self) -> dict:
        """Converts query to JSON object
        Returns:
            dict: return json obj
        """
        json_object = {
            'discoveryQueries':[query.to_json() for query in self.discovery_queries],
            'importMutations':[mutation.to_json() for mutation in self.import_mutations]
        }
        return json_object

    def generate_mutations(self) -> None:
        """Generate mutations based on deployment package
        """
        objs_required_export = self.deployment_package.get_obj_requiring_export_data()
        if (len(objs_required_export) != 0):
            raise(Exception("Not all objects have been exported."))
        # Generate the discovery queries
        import_query = Query()
        discovery_query = ImportDiscoveryQuery()
        for cvl_plan in self.deployment_package.deployment_plan.choice_lists:
            discovery_query.retrievals.append(cvl_plan.reference_id)
            self._add_cl_discovery_query(import_query, cvl_plan)
        for pt_plan in self.deployment_package.deployment_plan.property_templates:
            discovery_query.retrievals.append(pt_plan.reference_id)
            self._add_pt_discovery_query(import_query, pt_plan)
        for cd_plan in self.deployment_package.deployment_plan.class_definitions:
            discovery_query.retrievals.append(cd_plan.reference_id)
            self._add_cd_discovery_query(import_query, cd_plan)
        discovery_query.query = import_query.to_query()
        self.discovery_queries = [discovery_query]
        # Execute the discovery queries
        gql_req = GraphqlRequest(self.gql_connection)
        query_text = self.discovery_queries[0].query
        discovery_response = gql_req.execute_request(query_text)
        discovery_json = discovery_response.json()
        # DEBUG >>>
        # print("Discovery query response: ")
        # print(json.dumps(discjson, indent=4)) # <<<
        if "errors" in discovery_json:
            self._check_objs_not_found(self.discovery_queries[0].retrievals, discovery_json['errors'])
        # Generate the mutations
        ref_deployed_obj, id_deployed_obj = self.deployment_package.get_deployment_obj_maps()
        discovery_objects = discovery_json['data']
        mut = Mutation()
        mods = []
        # Note: eventually we will need to order the items in the batch based on their dependencies.
        # For now just add all of the property templates first then the class definitions.
        # TODO: Creating a property template in the same batch as adding a property
        # definition to a class definition not working in some environments. For now create 2
        # separate batches for the property templates and class definitions.
        total_objects = 0
        all_import_mutations = []
        for rid,discovery_object in discovery_objects.items():
            if rid.startswith("cl"):
                cvl_plan:ChoiceListPlan = ref_deployed_obj[rid]
                mods.append(cvl_plan.reference_id)
                self._add_cl_mutation(mut, cvl_plan, discovery_object)
                total_objects += 1
        if len(mut.outputItems) > 0:
            import_mut = ImportMutation(mods, mut.to_query(), "Adding or updating choice lists")
            all_import_mutations.append(import_mut)
        mods = []
        mut = Mutation()
        for rid,discovery_object in discovery_objects.items():
            if rid.startswith("pt"):
                pt_plan:PropertyTemplatePlan = ref_deployed_obj[rid]
                mods.append(pt_plan.reference_id)
                self._add_pt_mutation(mut, pt_plan, discovery_object)
                total_objects += 1
        if len(mut.outputItems) > 0:
            import_mut = ImportMutation(mods, mut.to_query(), "Adding or updating property templates")
            all_import_mutations.append(import_mut)
        next_batch = True
        super_class_ids = []
        new_batch = discovery_objects
        mutation_with_object_pd = Mutation()
        mods_with_object_pd=[]

        while next_batch is True:
            next_batch = False
            cds_list = {}
            mods = []
            mut = Mutation()

            current_super_class_ids = []
            for rid, discovery_object in new_batch.items():
                if rid.startswith("cd"):
                    cd_plan:ClassDefinitionPlan = ref_deployed_obj[rid]
                    can_execute = self._add_cd_mutation(mut, cd_plan, discovery_object, super_class_ids,
                                                                  current_super_class_ids, mutation_with_object_pd, mods_with_object_pd)
                    if can_execute is True:
                        total_objects += 1
                        if len(mut.outputItems) > 0:
                            mods.append(cd_plan.reference_id)
                    else:
                        next_batch = True
                        need_to_do = {rid: discovery_object}
                        cds_list.update(need_to_do)
            new_batch = cds_list
            if len(mut.outputItems) > 0:
                import_mut = ImportMutation(mods, mut.to_query(), "Adding or updating class definitions")
                all_import_mutations.append(import_mut)
        #do the object valued PD class update
        if len(mutation_with_object_pd.outputItems) > 0:
            impmut_with_object_pd = ImportMutation(mods_with_object_pd, mutation_with_object_pd.to_query(), "Adding or updating object valued property definitions")
            all_import_mutations.append(impmut_with_object_pd)
        if len(discovery_objects.items()) != total_objects:
            print("Unexpected: " + str(len(discovery_objects.items())) + " items discovered but recognized " + str(total_objects))
        self.import_mutations = all_import_mutations

    def import_package(self, gen_mutations: bool = False) -> list[dict]:
        """import deployment package into import object
        Args:
            gen_mutations (bool, optional): generate mutations if it hasn't been generated.
                Defaults to False.
        Returns:
            list[dict]: list containing response of mutations
        """
        if gen_mutations:
            self.generate_mutations()
            
        if not self.import_mutations:
            raise(Exception("Import mutations must be generated first."))

        mut_resp_json = []
        for import_mut in self.import_mutations:
            gql_req = GraphqlRequest(self.gql_connection)
            mut_text = import_mut.mutation
            mut_resp = gql_req.execute_request(mut_text)
            mut_json = mut_resp.json()
            mut_resp_json.append(mut_json)
            # DEBUG >>>
            #print("Mutation response: ")
            #print(json.dumps(mutjson, indent=4)) # <<<
        return mut_resp_json

    def _add_cl_mutation(self, mut:Mutation, plan: ChoiceListPlan, discovery_objects:dict):
        export_cvl = plan.export_data
        data_type:TypeID = TypeID[export_cvl['dataType']]
        display_name:str = export_cvl['displayName']
        descriptive_text:str = export_cvl['descriptiveText']

        cl_input:ChoiceListInput = ChoiceListInput()
        ch_array = []
        for cv in export_cvl['choiceValues']:
            ch_input:ChoiceInput = self._choice_recur(cv, dict)
            ch_array.append(ch_input)
        choice_values=ChoiceListInput(replace=ch_array)

        cvl_props = ChoiceListPropertiesInput(
            displayName=display_name,
            descriptiveText=descriptive_text,
            dataType=data_type if discovery_objects is None else None,
            choiceValues=choice_values)
        cvl_out = ChoiceList().field_id().field_displayName()

        if discovery_objects is None:
            mut.field_admCreateChoiceList(repositoryIdentifier=self.object_store_name,
                                                id=plan.id, choiceListProperties=cvl_props, alias=plan.reference_id,
                                                fieldOutput=cvl_out)
        else:
            mut.field_admUpdateChoiceList(repositoryIdentifier=self.object_store_name,
                                                identifier=plan.id, choiceListProperties=cvl_props, alias=plan.reference_id,
                                                fieldOutput=cvl_out)

    def _choice_recur(self, value_exported, dict) -> ChoiceInput:
        ch_input = ChoiceInput()
        choice_type:ChoiceType = ChoiceType[value_exported['choiceType']]
        if choice_type == ChoiceType.INTEGER or choice_type == ChoiceType.STRING:
            display_names_list = self._handle_loc_str_list(value_exported['displayNames'])
            display_names_val = LocalizedStringListInput(replace=display_names_list)
            ch_input = ChoiceInput(insertAction=InsertDependentActionInput(),
                                          choiceIntegerValue=self._exported_or_null_val(value_exported, 'choiceIntegerValue') ,
                                            choiceStringValue=self._exported_or_null_val(value_exported, 'choiceStringValue') ,
                                            choiceValues=NULL_VALUE,

                                            displayNames=display_names_val,
                                            choiceType=choice_type )
        else:
            cv_list = []
            for cv in value_exported['choiceValues']:
                one_input:ChoiceInput = self._choice_recur( cv, dict)
                cv_list.append(one_input)
            ch_input = ChoiceInput(insertAction=InsertDependentActionInput(),
                                          displayName=value_exported['displayName'],

                                            choiceType=choice_type,
                                            choiceValues = ChoiceListInput(replace=cv_list))
        return ch_input
    def _add_pt_mutation(self, mut:Mutation, plan:PropertyTemplatePlan, discovery_obj:dict):
        export_pt = plan.export_data
        data_type:TypeID = TypeID[export_pt['dataType']]
        display_name_list = self._handle_loc_str_list(export_pt['displayNames'])
        display_name_val = LocalizedStringListInput(replace=display_name_list)
        desc_texts_list = self._handle_loc_str_list(export_pt['descriptiveTexts'])
        desc_texts_val = LocalizedStringListInput(replace=desc_texts_list)
        pt_props:PropertyTemplatePropertiesInput = PropertyTemplatePropertiesInput(
            cardinality=Cardinality[export_pt['cardinality']] if discovery_obj is None else None,
            descriptiveTexts=desc_texts_val,
            displayNames=display_name_val,
            isHidden=self._exported_or_null_val(export_pt, 'isHidden'),
            isNameProperty=self._exported_or_null_val(export_pt, 'isNameProperty') if data_type != TypeID.OBJECT else None,
            isValueRequired=self._exported_or_null_val(export_pt, 'isValueRequired'),
            modificationAccessRequired=self._exported_or_null_val(export_pt, 'modificationAccessRequired'),
            settability=PropertySettability[export_pt['settability']] if export_pt['settability'] is not None else NULL_VALUE,
            symbolicName=export_pt['symbolicName'])
        if data_type == TypeID.BINARY:
            sub_binary = SubPropertyTemplateBinaryPropertiesInput(
                propertyDefaultBinary=self._exported_or_null_val(export_pt, 'propertyDefaultBinary'),
                maximumLengthBinary=self._exported_or_null_val(export_pt, 'maximumLengthBinary')
            )
            pt_props.subPropertyTemplateBinaryProperties = sub_binary
        elif data_type == TypeID.BOOLEAN:
            sub_bool = SubPropertyTemplateBooleanPropertiesInput(
                propertyDefaultBoolean=self._exported_or_null_val(export_pt, 'propertyDefaultBoolean')
            )
            pt_props.subPropertyTemplateBooleanProperties = sub_bool
        elif data_type == TypeID.DATE:
            sub_datetime = SubPropertyTemplateDateTimePropertiesInput(
                propertyDefaultDateTime=self._exported_or_null_val(export_pt, 'propertyDefaultDateTime'),
                propertyMaximumDateTime=self._exported_or_null_val(export_pt, 'propertyMaximumDateTime'),
                propertyMinimumDateTime=self._exported_or_null_val(export_pt, 'propertyMinimumDateTime')
            )
            pt_props.subPropertyTemplateDateTimeProperties=sub_datetime
        elif data_type == TypeID.DOUBLE:
            sub_float = SubPropertyTemplateFloat64PropertiesInput(
                propertyDefaultFloat64=self._exported_or_null_val(export_pt, 'propertyDefaultFloat64'),
                propertyMaximumFloat64=self._exported_or_null_val(export_pt, 'propertyMaximumFloat64'),
                propertyMinimumFloat64=self._exported_or_null_val(export_pt, 'propertyMinimumFloat64')
            )
            pt_props.subPropertyTemplateFloat64Properties=sub_float
        elif data_type == TypeID.GUID:
            sub_id = SubPropertyTemplateIdPropertiesInput(
                propertyDefaultId=self._exported_or_null_val(export_pt, 'propertyDefaultId')
            )
            pt_props.subPropertyTemplateIdProperties=sub_id
        elif data_type == TypeID.LONG:
            sub_int = SubPropertyTemplateInteger32PropertiesInput(
                propertyDefaultInteger32=self._exported_or_null_val(export_pt, 'propertyDefaultInteger32'),
                propertyMaximumInteger32=self._exported_or_null_val(export_pt, 'propertyMaximumInteger32'),
                propertyMinimumInteger32=self._exported_or_null_val(export_pt, 'propertyMinimumInteger32')
            )
            pt_props.subPropertyTemplateInteger32Properties=sub_int
        elif data_type == TypeID.STRING:
            sub_str = SubPropertyTemplateStringPropertiesInput(
                propertyDefaultString=self._exported_or_null_val(export_pt, 'propertyDefaultString'),
                maximumLengthString=self._exported_or_null_val(export_pt, 'maximumLengthString')
            )
            pt_props.subPropertyTemplateStringProperties=sub_str
        elif data_type == TypeID.OBJECT:
            sub_str = SubPropertyTemplateObjectPropertiesInput(
                allowsForeignObject=self._exported_or_null_val(export_pt, 'allowsForeignObject'),

            )
            pt_props.subPropertyTemplateObjectProperties=sub_str
        else:
            print("Unexpected data type encountered: " + str(data_type))
        #add CVL if the PT has it
        cvl = export_pt['choiceList']
        if cvl is not None:
            pt_props.choiceList=ObjectReferenceInput(identifier=cvl['id'])

        pt_out = PropertyTemplate().field_id().field_symbolicName()
        if discovery_obj is None:
            mut.field_admCreatePropertyTemplate(repositoryIdentifier=self.object_store_name, dataType=data_type,
                                                id=plan.id, propertyTemplateProperties=pt_props, alias=plan.reference_id, fieldOutput=pt_out)
        else:
            mut.field_admUpdatePropertyTemplate(repositoryIdentifier=self.object_store_name, identifier=plan.id,
                                                propertyTemplateProperties=pt_props, alias=plan.reference_id, fieldOutput=pt_out)

    def _add_cd_mutation(self, mut:Mutation, plan:ClassDefinitionPlan, discovery_object:dict, super_class_ids,
                                    current_batch_super_class_ids, mut_with_object_pd:Mutation, mods_with_object_pd:list[str]=None) -> bool:
        if mods_with_object_pd is None:
            mods_with_object_pd = []
        export_cd = plan.export_data
        #skip system class for now
        if export_cd['isSystemOwned'] is True:
            super_class_ids.append(plan.id)
            return True
        super_class = export_cd['superClassDefinition']
        if super_class is not None:
            #check if super class is deployed
            if super_class['id'] in super_class_ids and super_class['id'] not in current_batch_super_class_ids:
                #add ourself to deployed
                #superclassIds.append(plan.id)
                #superClassIdsInCurrentBatch.append(plan.id)
                pass
            else:
                #wait for next batch
                return False
        display_name_list = self._handle_loc_str_list(export_cd['displayNames'])
        display_name_val = LocalizedStringListInput(replace=display_name_list)
        desc_texts_list = self._handle_loc_str_list(export_cd['descriptiveTexts'])
        desc_texts_val = LocalizedStringListInput(replace=desc_texts_list)
        pd_exist = set()
        if discovery_object is not None:
            for discpd in discovery_object['propertyDefinitions'][discovery_object['protectedPropertyCount']:]:
                pd_exist.add(discpd['primaryId'])
        #print("Property definitions exist in existing object:")
        #print(str(pdsexist))
        pd_list = []
        pd_list_with_object_pd = []
        is_mut_with_object_pd = False
        for export_pd in export_cd['propertyDefinitions']:
            if export_pd['propertyTemplate'] is None:
                print("Encountered property definition in export data without a property template: " + export_pd['name'])
                continue
            data_type:TypeID = TypeID[export_pd['dataType']]
            prim_id = export_pd['propertyTemplate']['id']
            #print("Property definition primary id: " + primid)
            is_name_prop = self._exported_or_null_val(export_pd, 'isNameProperty')
            if prim_id in pd_exist and data_type == TypeID.OBJECT:
                is_name_prop = None
            pd_input = PropertyDefinitionInput(
                copyToReservation=self._exported_or_null_val(export_pd, 'copyToReservation'),
                isNameProperty=is_name_prop,
                isValueRequired=self._exported_or_null_val(export_pd, 'isValueRequired'),
                isHidden=self._exported_or_null_val(export_pd, 'isHidden'),
                modificationAccessRequired=self._exported_or_null_val(export_pd, 'modificationAccessRequired'),
                settability=PropertySettability[export_pd['settability']] if export_pd['settability'] is not None else NULL_VALUE,
            )

            if prim_id not in pd_exist:
                pd_input.propertyTemplate=ObjectReferenceInput(identifier=prim_id)
            else:
                pd_input.updateAction=UpdateDependentActionInput(itemReference=DependentItemReferenceInput(identifier=prim_id))
            if data_type == TypeID.BINARY:
                sub_binary = SubPropertyDefinitionBinaryInput(
                    propertyDefaultBinary=self._exported_or_null_val(export_pd, 'propertyDefaultBinary'),
                    maximumLengthBinary=self._exported_or_null_val(export_pd, 'maximumLengthBinary')
                )
                pd_input.subPropertyDefinitionBinary = sub_binary
            elif data_type == TypeID.BOOLEAN:
                sub_bool = SubPropertyDefinitionBooleanInput(
                    propertyDefaultBoolean=self._exported_or_null_val(export_pd, 'propertyDefaultBoolean')
                )
                pd_input.subPropertyDefinitionBoolean = sub_bool
            elif data_type == TypeID.DATE:
                sub_datetime = SubPropertyDefinitionDateTimeInput(
                    propertyDefaultDateTime=self._exported_or_null_val(export_pd, 'propertyDefaultDateTime'),
                    propertyMaximumDateTime=self._exported_or_null_val(export_pd, 'propertyMaximumDateTime'),
                    propertyMinimumDateTime=self._exported_or_null_val(export_pd, 'propertyMinimumDateTime')
                )
                pd_input.subPropertyDefinitionDateTime=sub_datetime
            elif data_type == TypeID.DOUBLE:
                sub_float = SubPropertyDefinitionFloat64Input(
                    propertyDefaultFloat64=self._exported_or_null_val(export_pd, 'propertyDefaultFloat64'),
                    propertyMaximumFloat64=self._exported_or_null_val(export_pd, 'propertyMaximumFloat64'),
                    propertyMinimumFloat64=self._exported_or_null_val(export_pd, 'propertyMinimumFloat64')
                )
                pd_input.subPropertyDefinitionFloat64=sub_float
            elif data_type == TypeID.GUID:
                sub_id = SubPropertyDefinitionIdInput(
                    propertyDefaultId=self._exported_or_null_val(export_pd, 'propertyDefaultId')
                )
                pd_input.subPropertyDefinitionId=sub_id
            elif data_type == TypeID.LONG:
                sub_int = SubPropertyDefinitionInteger32Input(
                    propertyDefaultInteger32=self._exported_or_null_val(export_pd, 'propertyDefaultInteger32'),
                    propertyMaximumInteger32=self._exported_or_null_val(export_pd, 'propertyMaximumInteger32'),
                    propertyMinimumInteger32=self._exported_or_null_val(export_pd, 'propertyMinimumInteger32')
                )
                pd_input.subPropertyDefinitionInteger32=sub_int
            elif data_type == TypeID.STRING:
                sub_str = SubPropertyDefinitionStringInput(
                    propertyDefaultString=self._exported_or_null_val(export_pd, 'propertyDefaultString'),
                    maximumLengthString=self._exported_or_null_val(export_pd, 'maximumLengthString')
                )
                pd_input.subPropertyDefinitionString=sub_str
            elif data_type == TypeID.OBJECT:
                #wait until all others are processed
                sub_obj = SubPropertyDefinitionObjectInput(
                    requiredClassId=self._exported_or_null_val(export_pd, 'requiredClassId'),
                    reflectivePropertyId=self._exported_or_null_val(export_pd, 'reflectivePropertyId')
                )
                #pdinp.subPropertyDefinitionObject=subobj
                if prim_id not in pd_exist: # only update object valued PD's subobj if this PD does not exist
                    is_mut_with_object_pd = True
                    pd_input.subPropertyDefinitionObject=sub_obj
            else:
                print("Unexpected data type encountered: " + str(data_type))
            if data_type != TypeID.OBJECT:
                pd_list.append(pd_input)
            else:
                #if it's an update on classdef and this obj valued PD already exists, we can update it without update the reqClass
                if prim_id in pd_exist:
                    pd_list.append(pd_input)
                mods_with_object_pd.append(plan.reference_id+"_object_pd_update")
                pd_list_with_object_pd.append(pd_input)

        cd_props:ClassDefinitionPropertiesInput = ClassDefinitionPropertiesInput(
            allowsInstances=self._exported_or_null_val(export_cd, 'allowsInstances'),
            defaultRetentionPeriod=self._exported_or_null_val(export_cd, 'defaultRetentionPeriod'),
            retentionPeriodUnits=DurationUnits[export_cd['retentionPeriodUnits']] if export_cd['retentionPeriodUnits'] is not None else NULL_VALUE,
            symbolicName=export_cd['symbolicName'],
            descriptiveTexts=desc_texts_val,
            displayNames=display_name_val,
            propertyDefinitions=PropertyDefinitionListInput(modify=pd_list)
        ) if export_cd['isSystemOwned'] is False else None

        cd_props_with_object_pd:ClassDefinitionPropertiesInput = ClassDefinitionPropertiesInput(
            allowsInstances=self._exported_or_null_val(export_cd, 'allowsInstances'),
            defaultRetentionPeriod=self._exported_or_null_val(export_cd, 'defaultRetentionPeriod'),
            retentionPeriodUnits=DurationUnits[export_cd['retentionPeriodUnits']] if export_cd['retentionPeriodUnits'] is not None else NULL_VALUE,
            symbolicName=export_cd['symbolicName'],
            descriptiveTexts=desc_texts_val,
            displayNames=display_name_val,
            propertyDefinitions=PropertyDefinitionListInput(modify=pd_list_with_object_pd)
        ) if export_cd['isSystemOwned'] is False else None

        cd_out = ClassDefinition().field_id().field_symbolicName()
        if discovery_object is None:
            super_cls_identifier = export_cd['superClassDefinition']['symbolicName']
            mut.field_admCreateClassDefinition(repositoryIdentifier=self.object_store_name, superclassIdentifier=super_cls_identifier,
                                               id=export_cd['id'], classDefinitionProperties=cd_props,
                                               alias=plan.reference_id, fieldOutput=cd_out)
            if is_mut_with_object_pd is True:
                #add an update
                mut_with_object_pd.field_admUpdateClassDefinition(repositoryIdentifier=self.object_store_name, identifier=plan.id,
                                               classDefinitionProperties=cd_props_with_object_pd, alias=plan.reference_id+"_object_pd_update",
                                               fieldOutput=cd_out)
        else:
            mut.field_admUpdateClassDefinition(repositoryIdentifier=self.object_store_name, identifier=plan.id,
                                               classDefinitionProperties=cd_props, alias=plan.reference_id,
                                               fieldOutput=cd_out)
            if is_mut_with_object_pd is True:
                mut_with_object_pd.field_admUpdateClassDefinition(repositoryIdentifier=self.object_store_name, identifier=plan.id,
                                               classDefinitionProperties=cd_props_with_object_pd, alias=plan.reference_id+"_object_pd_update",
                                               fieldOutput=cd_out)
        super_class_ids.append(plan.id)
        current_batch_super_class_ids.append(plan.id)
        return True
    def _handle_loc_str_list(self, explist:list[dict]) -> list[LocalizedStringInput]:
        # replace only supported for now. All localized string inputs are to insert new objects
        locstrinplist = []
        for explocstr in explist:
            locstrinp = LocalizedStringInput(
                localeName=explocstr['localeName'],
                localizedText=explocstr['localizedText']
            )
            locstrinplist.append(locstrinp)
        return locstrinplist


    def _exported_or_null_val(self, expobj:dict, attrname:str):
        return expobj[attrname] if expobj[attrname] is not None else NULL_VALUE

    def _check_objs_not_found(self, retrievals:list[str], resperrs:list[dict]):
        for resperr in resperrs:
            if "path" in resperr and len(resperr['path']) == 1 and resperr['path'][0] in retrievals:
                #print("Found error for " + resperr['path'][0])
                if resperr['extensions']['statusCode'] != "404":
                    raise Exception(resperr['extensions']['message'])

    def _add_cl_discovery_query(self, qry:Query, plan:ChoiceListPlan) -> None:
        cvl_out = ChoiceList()
        cvl_out.field_id()\
              .field_displayName()
        qry.field_choiceList(repositoryIdentifier=self.object_store_name,
                            identifier=plan.id, alias=plan.reference_id,
                            fieldOutput=cvl_out)
    def _add_pt_discovery_query(self, qry:Query, plan:PropertyTemplatePlan) -> None:
        prop_template_out = PropertyTemplate()
        prop_template_out.field_id()\
                    .field_symbolicName()
        qry.field_admPropertyTemplate(repositoryIdentifier=self.object_store_name,
                                      identifier=plan.id, alias=plan.reference_id,
                                      fieldOutput=prop_template_out)

    def _add_cd_discovery_query(self, qry:Query, plan:ClassDefinitionPlan) -> None:
        prop_def_out = PropertyDefinition()
        prop_def_out.field_id()\
                  .field_symbolicName()\
                  .field_primaryId()
        class_def_out = ClassDefinition()
        class_def_out.field_id()\
                 .field_symbolicName()\
                 .field_protectedPropertyCount()\
                 .field_propertyDefinitions(fieldOutput=prop_def_out)
        qry.field_admClassDefinition(repositoryIdentifier=self.object_store_name,
                                     identifier=plan.id, alias=plan.reference_id,
                                     fieldOutput=class_def_out)
