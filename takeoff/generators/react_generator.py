from .base_generator import BaseGenerator

class ReactGenerator(BaseGenerator):
    def __init__(self, name, subtype, options):
        self.name = name
        self.subtype = subtype

    def run(self):
        self.setup()
        print(f"Running React Project Generator: {self.name}")