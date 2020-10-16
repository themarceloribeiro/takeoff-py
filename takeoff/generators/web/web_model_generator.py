import os
from jinja2 import Template
from ..generator_base import GeneratorBase
from pathlib import Path

class WebModelGenerator(GeneratorBase):
    def __init__(self, name, options):
        self.name = name
        self.options = options
        self.model_name = ''
        self.model_attributes = []

    def project_folder(self):
        return f"dist/{self.name}/web/{self.name}"

    def run(self):
        self.model_name = self.options.pop(0)
        print(f"Running Web Model Generator: {self.name} : {self.model_name}")
        for attribute in self.options:
            parts = attribute.split(':')
            self.model_attributes.append({
                'name': parts[0], 
                'type': parts[1], 
                'class': self.attribute_class(parts[1]),
                'field_extra': self.attribute_field_extra(parts[1])
            })

        self.write_model_file()
        self.update_models_file()        
        self.generate_migration()
    
    def attribute_class(self, type):
        switcher = { 
            'string': 'CharField', 
            'integer': 'IntegerField'
        }   
        return switcher.get(type, 'CharField')
    
    def attribute_field_extra(self, type):
        switcher = { 
            'string': "default='', max_length=250", 
            'integer': 'default=0'
        }   
        return switcher.get(type, "default='', max_length=250")

    def write_model_file(self):
        template_path = '/Users/marcelo/work/takeoff/python/takeoff/takeoff/templates/web/model.template'
        destination_folder = f"{self.project_folder()}/main/models"
        os.system(f"mkdir -p {destination_folder}")
        Path(f"{destination_folder}/__init__.py").touch()
        destination = f"{destination_folder}/{self.model_name}.py"

        with open(template_path) as f:
            template_contents = f.read()

        template = Template(template_contents)
        contents = template.render(generator=self)
        
        with open(destination, 'w') as f:
            f.write(contents)

    def update_models_file(self):
        current_file = f"{self.project_folder()}/main/models/__init__.py"

        lines = list(open(current_file, 'r'))
        lines.append(f"from .{self.model_name} import {self.model_name.replace('_', ' ').title().replace(' ', '')}\n")
        
        with open(current_file, 'w') as file:
            file.writelines(lines)

    def models_last_line(self, lines):
        return len(lines)
    
    def generate_migration(self):
        os.system(f"cd {self.project_folder()} && python3 manage.py makemigrations")