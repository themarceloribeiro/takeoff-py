import os
import json
from .android_component_builder import AndroidComponentBuilder

class LabelBuilder(AndroidComponentBuilder):

    def __init__(self, options, component):
        super().__init__(options, component)
        self.constraints = {}
        self.name = ''
        self.text = ''
        self.text_align = 'left'
        self.font = {
            'face': 'Arial',
            'size': 20,
            'color': '#000000',
            'weight': 'normal'
        }
        self.lines = []        
        self.load_attributes()

    def load_lines(self):
        self.lines = [
            '   <TextView',
            f"      android:id=\"@+id/{self.name}\"",
            f"      android:text=\"{self.text}\"",
        ]
        
        if self.text_align != 'left':
            self.lines += [f"      android:textAlignment=\"{self.text_align}\""]
        
        self.lines += self.constraint_lines()
        self.lines += self.text_styling_lines()
        self.lines += ["      />\n"]

        return ("\n").join(self.lines)

    def text_styling_lines(self):
        return [
            f"      fontPath=\"font/{self.font['face']}.ttf\"",
            f"      android:textStyle=\"{self.font['weight']}\"",       
            f"      android:textSize=\"{self.font['size']}sp\"",
            f"      android:textColor=\"{self.font['color']}\""
        ]