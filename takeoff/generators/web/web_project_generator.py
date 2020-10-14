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
    
    def create_django_project(self):
        print('Creating Django Project')
        os.system(f"cd dist/web && django-admin startproject {self.name}")

    def create_structure_folders(self):
        fullpath = f"dist/web/"
        print(f"    Creating Web Folder: {fullpath}")            
        os.system(f"mkdir -p {fullpath}")