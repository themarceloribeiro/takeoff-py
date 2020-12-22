import os
from jinja2 import Template
from .android_base_generator import AndroidBaseGenerator
from ...builders.android import *
from pathlib import Path
from shutil import copyfile

class AndroidComponentGenerator(AndroidBaseGenerator):

    def __init__(self, name, options):
        super().__init__(name, options)
        self.component_type = self.options.pop(0)

    def component_builder(self):
        klass_name = f"{self.component_type.replace('_', ' ').title()} Builder".replace(' ', '')
        return eval(f"{klass_name}(self.options)")        

    def run(self):
        self.setup()
        print(f">>> Running Android Component Generator: {self.component_type}")
        builder = self.component_builder()
        builder.generator = self
        builder.build()