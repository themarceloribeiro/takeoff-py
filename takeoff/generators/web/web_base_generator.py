import os
from jinja2 import Template
from ..generator_base import GeneratorBase
from pathlib import Path

class WebBaseGenerator(GeneratorBase):
    def __init__(self, name, options):
        super().__init__(name, options)

    def project_type(self):
        return 'web'