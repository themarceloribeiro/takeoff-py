from .generator_base import GeneratorBase

class IosProjectGenerator(GeneratorBase):
    def __init__(self, name, options):
        self.name = name

    def run(self):
        self.setup()
        print(f"Running iOS Project Generator: {self.name}")