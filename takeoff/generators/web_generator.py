import os
from jinja2 import Template
from .generator_base import GeneratorBase
from .web.web_project_generator import WebProjectGenerator
from .web.web_model_generator import WebModelGenerator

class WebGenerator(GeneratorBase):
    def __init__(self, name, subtype, options):
        self.name = name
        self.subtype = subtype
        self.options = options

    def run(self):
        self.setup()
        klass_name = f"Web{self.subtype.replace('_', ' ').title()} Generator".replace(' ', '')
        generator = eval(f"{klass_name}(self.name, self.options)")
        generator.run()