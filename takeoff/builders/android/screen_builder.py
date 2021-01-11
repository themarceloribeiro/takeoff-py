import os
import json
import itertools
from . import *
from .image_builder import ImageBuilder
from .list_builder import ListBuilder
from .label_builder import LabelBuilder
from .text_field_builder import TextFieldBuilder
from .button_builder import ButtonBuilder
from .facebook_button_builder import FacebookButtonBuilder
from .transition_action_builder import TransitionActionBuilder

class ScreenBuilder(AndroidComponentBuilder):
    def build(self):
        self.json_file = ''
        self.assets_path = ''
        self.data = {}
        self.load_attributes()
        self.copy_assets()
        self.load_json()
        self.render_layout_file()
        self.render_fragment_file()

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
        lines = [eval(f"self.start_{self.data['layout']}_layout()")]
        lines += list(itertools.chain(*list(map(lambda x: self.component_lines(x), self.data['components']))))
        lines += [eval(f"self.finish_{self.data['layout']}_layout()")]

        with open(destination, 'w') as file:
            file.writelines(lines)
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

    def render_fragment_file(self):
        group_folder = f"{self.generator.project_folder()}/app/src/main/java/{self.generator.android_prefix.replace('.', '/')}/{self.data['group']}"
        destination = f"{group_folder}/{self.generator.camelize(self.data['name'])}Fragment.kt"
        protocols = self.fragment_protocols()

        lines = f"""
package {self.generator.android_prefix}.{self.data['group']}

import android.os.Bundle
import android.view.*
import {self.generator.android_prefix}.R
import {self.generator.android_prefix}.base.BaseFragment
{self.list_protocol_imports()}

class {self.generator.camelize(self.data['name'])}Fragment : BaseFragment(){protocols} {'{'}
{self.fragment_protocol_implementations()}
{self.build_actions()}
{'}'}"""

        with open(destination, 'w') as file:
            file.writelines(lines)
        print("Fragment file: OK;")

    def fragment_protocols(self):
      protocols = []
      protocols_string = ""

      for component in self.data["components"]:
        if component['type'] == 'list':
          protocols += ["AdapterView.OnItemClickListener"]

      if len(protocols) > 0:
        protocols_string = f", {(', ').join(protocols)}"

      return protocols_string

    def fragment_protocol_imports(self):
      for component in self.data["components"]:
        if component['type'] == 'list':
          return self.list_protocol_imports()

      return ""

    def fragment_protocol_implementations(self):
      for component in self.data["components"]:
        if component['type'] == 'list':
          return self.list_protocol_lines(component)

      return ""

    def list_protocol_imports(self):
      return ("\n").join([
        "import android.widget.AdapterView"
      ])

    def list_protocol_lines(self, component):
      return f"""
    override fun onItemClick(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {'{'}
      {component["list_view_action"]}()
    {'}'}"""

    def build_actions(self):
      return ("\n").join(list(map(lambda x: self.build_action(x), self.data['actions'])))

    def build_action(self, action):
      builder = eval(f"{self.generator.camelize(action['type'])}ActionBuilder(action)")
      builder.generator = self.generator
      return builder.load_lines()