from ...builders.component_builder import ComponentBuilder

class AndroidActionBuilder(ComponentBuilder):
    def __init__(self, options, component=None):
        self.options = options


    def build(self):
        print("Building...")