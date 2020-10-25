import os
from jinja2 import Template
from .web_base_generator import WebBaseGenerator
from pathlib import Path

class WebAuthenticationGenerator(WebBaseGenerator):
    def __init__(self, name, options):
        super().__init__(name, options)

    def run(self):
        print(f"Running Web Authentication Generator: {self.name}")
