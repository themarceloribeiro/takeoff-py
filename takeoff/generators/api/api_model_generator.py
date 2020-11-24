import os
from jinja2 import Template
from .api_base_generator import ApiBaseGenerator
from pathlib import Path

class ApiModelGenerator(ApiBaseGenerator):
    def __init__(self, name, options):
        super().__init__(name, options)

    def run(self):
        print(f"Running API Model Generator: {self.name}")