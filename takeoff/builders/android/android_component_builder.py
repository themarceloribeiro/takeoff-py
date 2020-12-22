from ...builders.component_builder import ComponentBuilder

class AndroidComponentBuilder(ComponentBuilder):
    def __init__(self, options):
        self.options = options

    def load_attributes(self):
        for attribute in self.options:
            parts = attribute.split('=')
            setattr(self, parts[0], parts[1])

    def build(self):
        print("Building...")