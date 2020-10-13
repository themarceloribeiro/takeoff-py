from jinja2 import Template
from .generators.android_project_generator import AndroidProjectGenerator
from .generators.ios_project_generator import IosProjectGenerator
from .generators.api_project_generator import ApiProjectGenerator
from .generators.react_project_generator import ReactProjectGenerator

class Generator:
    def __init__(self, arguments):
        if len(arguments) < 2:
            self.print_instructions()
        else:
            self.generator_type = arguments.pop(0)
            self.name = arguments.pop(0)
            self.options = arguments

    def print_instructions(self):
        print('This package helps with your project takeoff by creating views, models and project structure based off of JSON files')
    
    def run(self):
        generator = self.get_generator()
        generator.run()
    
    def get_generator(self):
        klass_name = ''.join(x for x in f"{self.generator_type.replace('_', ' ')} Generator".title() if not x.isspace())
        return eval(f"{klass_name}(self.name)")