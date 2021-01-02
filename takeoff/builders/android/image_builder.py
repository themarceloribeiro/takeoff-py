import os
import json
from .android_component_builder import AndroidComponentBuilder

class ImageBuilder(AndroidComponentBuilder):

    def __init__(self, options, component):
        super().__init__(options, component)
        self.constraints = {}
        self.name = ''
        self.src = ''
        self.load_attributes()

    def load_lines(self):
        self.lines = [
            '   <ImageView',
            f"      android:id=\"@+id/{self.name}\"",
            f"      android:contentDescription=\"{self.generator.camelize(self.name)}\"",
            f"      android:src=\"@drawable/{self.src.split('.')[0]}\"",
        ]
        self.lines += self.constraint_lines()
        self.lines += ["      />\n"]

        return ("\n").join(self.lines)