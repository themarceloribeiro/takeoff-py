from .generator_base import GeneratorBase

class ReactProjectGenerator(GeneratorBase):
    def __init__(self, name):
        self.name = name

    def run(self):
        self.setup()
        print(f"Running React Project Generator: {self.name}")