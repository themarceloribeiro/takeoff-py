import os
import json
from .android_action_builder import AndroidActionBuilder

class TransitionActionBuilder(AndroidActionBuilder):

    def __init__(self, options):
        super().__init__(options)
        self.name = options['name']
        self.type = options['type']
        self.attributes = options['attributes']

    def load_lines(self):
      print(self.options)
      self.lines = [
        f"    fun {self.name}() {'{'}",
        '    }'
      ]

      return ("\n").join(self.lines)