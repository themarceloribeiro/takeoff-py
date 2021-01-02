import os
import json
from .android_component_builder import AndroidComponentBuilder

class ButtonBuilder(AndroidComponentBuilder):

    def __init__(self, options, component):
        super().__init__(options, component)
        self.constraints = {}
        self.name = ''
        self.text = ''
        self.text_align = 'center'
        self.background_color = '#000000'
        self.text_color = '#ffffff'
        self.lines = []        
        self.load_attributes()

    def load_lines(self):
        self.lines = [
            '   <Button',
            f"      android:id=\"@+id/{self.name}\"",
            f"      android:text=\"{self.text}\"",
            f"      android:textAlignment=\"{self.text_align}\"",
            f"      android:textColor=\"{self.text_color}\"",
            f"      android:background=\"{self.background_color}\"",
            
        ]
        self.lines += self.constraint_lines()
        self.lines += ["      />\n"]

        return ("\n").join(self.lines)