import os
import json
import itertools
from . import *
from .image_builder import ImageBuilder
from .label_builder import LabelBuilder
from .text_field_builder import TextFieldBuilder
from .button_builder import ButtonBuilder
from .facebook_button_builder import FacebookButtonBuilder

class ScreenBuilder(AndroidComponentBuilder):
    def build(self):
        self.json_file = ''
        self.assets_path = ''
        self.data = {}
        self.lines = []
        self.load_attributes()
        self.copy_assets()
        self.load_json()
        self.render_layout_file()
    
    def copy_assets(self):
        if self.assets_path == '':
            return
        files = os.listdir(f"{self.assets_path}/images")
        destination = f"{self.generator.project_folder()}/app/src/main/res/drawable/"
        os.system(f"mkdir -p {destination}")
        for file in files:
            os.system(f"cp {self.assets_path}/images/{file} {destination}")

        font_files = os.listdir(f"{self.assets_path}/fonts")
        destination = f"{self.generator.project_folder()}/app/src/main/assets/fonts/"
        os.system(f"mkdir -p {destination}")
        for file in font_files:
            os.system(f"cp {self.assets_path}/fonts/{file} {destination}")
    
    def load_json(self):
        self.data = json.loads(("").join(list(open(self.json_file, 'r'))))
    
    def render_layout_file(self):
        destination = f"{self.generator.project_folder()}/app/src/main/res/layout/{self.data['name']}.xml"
        self.lines += [eval(f"self.start_{self.data['layout']}_layout()")]
        self.lines += list(itertools.chain(*list(map(lambda x: self.component_lines(x), self.data['components']))))
        self.lines += [eval(f"self.finish_{self.data['layout']}_layout()")]

        with open(destination, 'w') as file:
            file.writelines(self.lines)
        print("Layout file: OK;")
    
    def component_lines(self, component):
        klass = f"{self.generator.camelize(component['type'])}Builder"
        builder = eval(f"{klass}(None, component)")
        builder.generator = self.generator
        return builder.load_lines()

    def start_constraint_layout(self):
        return f"""<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:id="@+id/{self.generator.camelize(self.data['name'])}Layout">\n"""
    
    def finish_constraint_layout(self):
        return "</androidx.constraintlayout.widget.ConstraintLayout>"