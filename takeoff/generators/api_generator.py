import os
from jinja2 import Template
from .base_generator import BaseGenerator
from .api import *

class ApiGenerator(BaseGenerator):
    def __init__(self, name, subtype, options):
        self.name = name
        self.subtype = subtype
        self.options = options

    def generator_class_prefix(self):
        return "Api"

    def generator(self):
        klass_name = f"{self.generator_class_prefix()}{self.subtype.replace('_', ' ').title()} Generator".replace(' ', '')
        return eval(f"{klass_name}(self.name, self.options)")
