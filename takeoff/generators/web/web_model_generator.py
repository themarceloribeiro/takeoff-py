import os
from jinja2 import Template
from ..generator_base import GeneratorBase

class WebModelGenerator(GeneratorBase):
    def __init__(self, name, options):
        self.name = name

    def run(self):
        print(f"Running Web Model Generator: {self.name}")