import os
import json
from .android_component_builder import AndroidComponentBuilder

class TextFieldBuilder(AndroidComponentBuilder):

    def __init__(self, options, component):
        super().__init__(options, component)
        self.constraints = {}
        self.secure = False
        self.name = ''
        self.text = ''
        self.input_type = 'text'
        self.lines = []        
        self.load_attributes()

    def load_lines(self):
        if self.secure:
            self.input_type = 'textPassword'

        self.lines = [
            '   <EditText',
            f"      android:id=\"@+id/{self.name}\"",
            f"      android:text=\"{self.text}\"",
            f"      android:inputType=\"{self.input_type}\"",
        ]
        
        if self.placeholder is not None:
            self.lines += [ f"      android:hint=\"{self.placeholder}\""]

        self.lines += self.constraint_lines()
        self.lines += ["      />\n"]

        return ("\n").join(self.lines)