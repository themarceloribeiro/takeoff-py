import os
from jinja2 import Template
from ..generator_base import GeneratorBase

class WebProjectGenerator(GeneratorBase):
    def __init__(self, name, options):
        self.name = name

    def run(self):
        self.setup()
        print(f"Running Web Project Generator: {self.name}")
        self.create_structure_folders()
        self.create_django_project()
        self.prepare_settings()
    
    def create_django_project(self):
        print('Creating Django Project')
        os.system(f"cd dist/{self.name}/web && django-admin startproject {self.name}")
        os.system(f"cd dist/{self.name}/web/{self.name} && python3 manage.py startapp main")

    def create_structure_folders(self):
        fullpath = f"dist/{self.name}/web/"
        print(f"    Creating Web Folder: {fullpath}")            
        os.system(f"mkdir -p {fullpath}")
    
    def prepare_settings(self):
        settings_file = f"dist/{self.name}/web/{self.name}/{self.name}/settings.py"
        lines = list(open(settings_file, 'r'))
        last_line = self.installed_apps_last_line(lines)
        lines.insert(last_line - 1, "    'main',\n")
        
        with open(settings_file, 'w') as file:
            file.writelines(lines)
    
    def installed_apps_last_line(self, lines):
        i = 0
        start = 0
        finish = 0

        for line in lines:
            i += 1
            if 'INSTALLED_APPS' in line:
                start = i
            if start > 0 and finish == 0 and ']' in line:
                finish = i

        return finish