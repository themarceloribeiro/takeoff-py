import os
import json
from .android_component_builder import AndroidComponentBuilder

class FacebookButtonBuilder(AndroidComponentBuilder):

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
            '   <com.facebook.login.widget.LoginButton',
            f"      android:id=\"@+id/{self.name}\""
            
        ]
        self.lines += self.constraint_lines()
        self.lines += ["      />\n"]

        return ("\n").join(self.lines)