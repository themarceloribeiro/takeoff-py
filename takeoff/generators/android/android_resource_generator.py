import os
from jinja2 import Template
from .android_base_generator import AndroidBaseGenerator
from pathlib import Path
from shutil import copyfile

class AndroidResourceGenerator(AndroidBaseGenerator):

    def __init__(self, name, options):
        super().__init__(name, options)
        self.entity_name = self.options.pop(0)
        self.entity_attributes = []

    def run(self):
        self.setup()
        print(f">>> Running Android Resource Generator: {self.entity_name}")
        self.load_resource_attributes()
        self.render_resource_form_fragment()
        self.render_resource_list_fragment()
        self.render_resource_list_adapter()
    
    def load_resource_attributes(self):
        entity_file = f"{self.project_folder()}/app/src/main/java/{self.android_prefix.replace('.', '/')}/models/{self.entity_name}.kt"
        lines = list(open(entity_file, 'r'))

        android_entity_attribute_types = [
            'Int?',
            'String?',
            'Date?',
        ]

        for line in lines:
            for field_type in android_entity_attribute_types:
                if f": {field_type} = " in line:
                    attribute_name = line.strip().split(":")[0].strip().replace('var ', '')
                    attribute_type = field_type.replace('?', '')
                    if attribute_name not in ['created_at', 'updated_at']:
                        attribute_definition = { 
                            'attribute_name': attribute_name, 
                            'attribute_type': attribute_type,
                            'field_type': self.field_type_for_attribute(attribute_type),
                            'to_string_modifier': self.to_string_modifier(attribute_type),
                            'from_string_modifier': self.from_string_modifier(attribute_type)
                        }

                        self.entity_attributes.append(attribute_definition)

    def to_string_modifier(self, attribute_type):
        if attribute_type == 'String':
            return ''
        elif attribute_type == 'Date':
            return f"?.to{attribute_type}String()"            
        else:
            return '.toString()'
    
    def from_string_modifier(self, attribute_type):
        if attribute_type == 'String':
            return ''
        else:
            return f".to{attribute_type}()"

    def field_type_for_attribute(self, attribute_type):
        types = {
            'Int': 'EditText',
            'String': 'EditText',
            'Date': 'EditText'
        }
        return types.get(attribute_type)

    def render_resource_form_fragment(self):
        package_path = self.android_prefix.replace('.', '/')
        template_path = f"{self.templates_path}/app/src/main/java/resource/ResourceFormFragment.kt.template"
        destination_folder = f"{self.project_folder()}/app/src/main/java/{package_path}/{self.entity_name}"
        os.system(f"mkdir -p {destination_folder}")
        destination = f"{destination_folder}/{self.camelize(self.entity_name)}FormFragment.kt"
        self.write_from_template(template_path, destination)

        xml_template_path = f"{self.templates_path}/app/src/main/java/resource/resource_form_fragment.xml.template"
        xml_destination_folder = f"{self.project_folder()}/app/src/main/res/layout"
        xml_destination = f"{xml_destination_folder}/{self.entity_name.lower()}_form_fragment.xml"
        self.write_from_template(xml_template_path, xml_destination)

    def render_resource_list_fragment(self):
        package_path = self.android_prefix.replace('.', '/')
        template_path = f"{self.templates_path}/app/src/main/java/resource/ResourceListFragment.kt.template"
        destination_folder = f"{self.project_folder()}/app/src/main/java/{package_path}/{self.entity_name}"
        destination = f"{destination_folder}/{self.camelize(self.entity_name)}ListFragment.kt"
        self.write_from_template(template_path, destination)

        xml_template_path = f"{self.templates_path}/app/src/main/java/resource/resource_list_fragment.xml.template"
        xml_destination_folder = f"{self.project_folder()}/app/src/main/res/layout"
        xml_destination = f"{xml_destination_folder}/{self.entity_name.lower()}_list_fragment.xml"
        self.write_from_template(xml_template_path, xml_destination)

        xml_item_template_path = f"{self.templates_path}/app/src/main/java/resource/resource_list_item.xml.template"
        xml_item_destination_folder = f"{self.project_folder()}/app/src/main/res/layout"
        xml_item_destination = f"{xml_item_destination_folder}/{self.entity_name.lower()}_list_item.xml"
        self.write_from_template(xml_item_template_path, xml_item_destination)

    def render_resource_list_adapter(self):
        package_path = self.android_prefix.replace('.', '/')
        template_path = f"{self.templates_path}/app/src/main/java/resource/ResourceListAdapter.kt.template"
        destination_folder = f"{self.project_folder()}/app/src/main/java/{package_path}/{self.entity_name}"
        destination = f"{destination_folder}/{self.camelize(self.entity_name)}ListAdapter.kt"
        self.write_from_template(template_path, destination)