import os
from jinja2 import Template
from .generator_base import GeneratorBase
from .android import *

class AndroidGenerator(GeneratorBase):
    def __init__(self, name, subtype, options):
        self.name = name
        self.subtype = subtype
        self.options = options

    def generator(self):
        klass_name = f"Android{self.subtype.replace('_', ' ').title()} Generator".replace(' ', '')
        return eval(f"{klass_name}(self.name, self.options)")

    def run(self):
        self.setup()
        self.generator().run()