import os
from jinja2 import Template
from .base_generator import BaseGenerator
from .api import *
from .android import *
from .web import *
import json

class ProjectGenerator(BaseGenerator):
    def __init__(self, json_file, subtype, options):
        self.data = {}
        self.name = ''
        self.json_file = json_file
        self.options = options

    def run(self):
        self.data = json.loads(("").join(list(open(self.json_file, 'r'))))        
        self.name = self.data['name']
        os.system(f"rm -rf dist/{self.name}")

        self.build_projects()
        self.build_authentication()
        self.build_entities()
        self.build_resources()
        self.build_screens()
        self.build_components()

    def build_projects(self):
        for platform in self.data['platforms']:
            print(f"Running Project Builder for {platform}")
            os.system(f"./takeoff-generate {platform}:project {self.name} database={self.data['database']}")

    def build_authentication(self):
        if self.data['authentication'] == None:
            return

        for platform in self.data['platforms']:
            print(f"Running Authentication Builder for {platform}")
            print(f"./takeoff-generate {platform}:authentication {self.name} facebook_auth={self.data['authentication']['facebook']} facebook_app_id={self.data['authentication']['facebook_app_id']} facebook_scheme={self.data['authentication']['facebook_scheme']}")
            os.system(f"./takeoff-generate {platform}:authentication {self.name} facebook_auth={self.data['authentication']['facebook']} facebook_app_id={self.data['authentication']['facebook_app_id']} facebook_scheme={self.data['authentication']['facebook_scheme']}")
    
    def build_entities(self):
        if self.data['entities'] == None:
            return

        for platform in self.data['platforms']:
            entity_type = 'model'
            if platform == 'android':
                entity_type = 'entity'

            print(f"Running Entities Builder for {platform}")
            for entity in self.data['entities']:
                attributes = (" ").join(list(map(lambda key: f"{key}:{entity['attributes'][key]}", entity['attributes'].keys())))
                os.system(f"./takeoff-generate {platform}:{entity_type} {self.name} {entity['name']} {attributes}")
    
    def build_resources(self):
        if self.data['resources'] == None:
            return

        for platform in self.data['platforms']:
            print(f"Running Resources Builder for {platform}")
            for resource in self.data['resources']:
                os.system(f"./takeoff-generate {platform}:resource {self.name} {resource}")
    
    def build_screens(self):
        print("Screens")
    
    def build_components(self):
        print("Components")