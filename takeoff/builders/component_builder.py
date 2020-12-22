import os
from jinja2 import Template
from pathlib import Path
from shutil import copyfile

class ComponentBuilder:
    def __init__(self, options):
        self.options = options
        self.generator = None

    def write_from_template(self, source, destination):
        with open(source) as f:
            template_contents = f.read()

        template = Template(template_contents)
        contents = template.render(generator=self.generator, builder=self)
        
        with open(destination, 'w') as f:
            f.write(contents)

    def load_attributes(self):
        for attribute in self.options:
            parts = attribute.split('=')
            setattr(self, parts[0], parts[1])
    
    def build(self):
        print("Building...")