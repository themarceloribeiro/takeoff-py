from .generator_base import GeneratorBase

class ApiProjectGenerator(GeneratorBase):
    def __init__(self, name, options):
        self.name = name

    def run(self):
        self.setup()
        print(f"Running API Project Generator: {self.name}")