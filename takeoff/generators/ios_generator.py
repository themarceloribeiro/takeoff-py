from .base_generator import BaseGenerator

class IosGenerator(BaseGenerator):
    def __init__(self, name, subtype, options):
        self.name = name
        self.subtype = subtype

    def run(self):
        self.setup()
        print(f"Running iOS Project Generator: {self.name}")