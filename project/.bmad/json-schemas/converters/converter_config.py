# -*- coding: utf-8 -*-

DOCUMENT_TYPE_CONVERTERS = {
    'project_brief': 'convert_project_brief',
    'prd': 'convert_prd',
    'architecture': 'convert_architecture',
    'front_end_architecture': 'convert_front_end_architecture',
    'component_specs': 'convert_component_specs',
    'data_models': 'convert_data_models',
    'api_reference': 'convert_api_reference',
    'tech_stack': 'convert_tech_stack',
    'environment': 'convert_environment',
}

SCHEMA_FILE_MAPPING = {
    'project_brief': 'schemas/project-brief-schema.json',
    'prd': 'schemas/prd-schema.json',
    'architecture': 'schemas/architecture-schema.json',
    'front_end_architecture': 'schemas/front-end-architecture-schema.json',
    'component_specs': 'schemas/component-specs-schema.json',
    'data_models': 'schemas/data-models-schema.json',
    'api_reference': 'schemas/api-reference-schema.json',
    'tech_stack': 'schemas/tech-stack-schema.json',
    'environment': 'schemas/environment-schema.json',
}
