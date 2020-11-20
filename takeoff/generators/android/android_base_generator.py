import os
from jinja2 import Template
from ..generator_base import GeneratorBase
from pathlib import Path

class AndroidBaseGenerator(GeneratorBase):
    def __init__(self, name, options):
        super().__init__(name, options)
        self.name = name
        self.options = options
        self.android_prefix = ''
        self.templates_path = f"{self.templates_path}/android"

        for option in options:
            if 'android_prefix' in option:
                self.android_prefix = option.split('=')[1]
        
        if self.android_prefix == '':
            self.android_prefix = f"com.{self.name}.app"            

        self.product_package = f"{self.android_prefix}.{self.name.replace(' ', '').lower()}"        

    def android_sdk_path(self):
        return "/Users/marcelo/Library/Android/sdk"

    def project_type(self):
        return 'android'

    def add_manifest_activity(self, activity):
        destination = f"{self.project_folder()}/app/src/main/AndroidManifest.xml"
        new_line = f"<activity android:name=\"{activity}\"/>\n"
        self.add_line_before_pattern(destination, new_line, 'EndActivities')

    def add_string_translation(self, key, value):
        destination = f"{self.project_folder()}/app/src/main/res/values/strings.xml"
        new_line = f"<string name=\{key}\">{value}</string>\n"
        self.add_line_before_pattern(destination, new_line, '/resources')
    
    def add_method_to_class(self, kotlin_class, method, identifier=''):
        destination = f"{self.project_folder()}/app/src/main/java/{self.android_prefix.replace('.', '/')}/{kotlin_class}"
        new_lines = method.split("\n")
        self.add_lines_before_last_line(destination, new_lines, identifier)
    
    def replace_lines_for_method(self, kotlin_class, method, lines):
        destination = f"{self.project_folder()}/app/src/main/java/{self.android_prefix.replace('.', '/')}/{kotlin_class}"
        self.replace_lines_for_block(destination, method, '}', lines)
    
    def add_attribute_to_entity(self, entity_name, attribute_name, attribute_type):
        destination = f"{self.project_folder()}/app/src/main/java/{self.android_prefix.replace('.', '/')}/models/{entity_name}.kt"
        new_line = f"var {attribute_name}: {attribute_type}? = null\n"
        self.add_line_before_pattern(destination, new_line, f"class {entity_name}")

        new_line = f"{attribute_name} = jsonObject.get(\"{attribute_name}\") as {attribute_type}\n"
        self.add_line_before_pattern(destination, new_line, f"EndFromJson")

        new_line = f"json.put(\"{attribute_name}\", {attribute_name})\n"
        self.add_line_before_pattern(destination, new_line, f"EndToJson")