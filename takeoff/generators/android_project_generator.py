from .generator_base import GeneratorBase

class AndroidProjectGenerator(GeneratorBase):
    def __init__(self, name):
        self.name = name

    def run(self):
        self.setup()
        print(f"Running Android Project Generator: {self.name}")