from ...builders.component_builder import ComponentBuilder

class AndroidComponentBuilder(ComponentBuilder):
    def __init__(self, options, component=None):
        self.options = options
        self.component = component
        self.width = None
        self.height = None
        self.lines = []

    def load_attributes(self, component=None):
        if self.options is not None:
            for attribute in self.options:
                parts = attribute.split('=')
                setattr(self, parts[0], parts[1])
        if self.component is not None:
            for key in self.component.keys():
                setattr(self, key, self.component[key])

    def constraint_lines(self):
        constraint_lines = []
        
        for constraint in self.constraints:
            constraint_lines += eval(f"self.{constraint['type']}_constraint_lines(constraint)")

        if self.width is None:
            self.width = 'match_parent'
            constraint_lines += [f"      android:layout_width=\"{self.width}\""]

        if self.height is None:
            self.height = 'wrap_content'
            constraint_lines += [f"      android:layout_height=\"{self.height}\""]

        return constraint_lines

    def translated_constraint_type(self, constraint_type):
        constraint_types = {
            'leading': 'left',
            'trailing': 'right',
            'top': 'top',
            'bottom': 'bottom'
        }
        return constraint_types[constraint_type]

    def standard_constraint_lines(self, constraint):
        related_view = constraint['related_view']
        constraint_type = self.generator.camelize(self.translated_constraint_type(constraint['type']))
        related_constraint_type = self.generator.camelize(self.translated_constraint_type(constraint['related_constraint']))

        if related_view != 'parent':
            related_view = f"@+id/{related_view}"

        lines = [
            f"      android:layout_margin{constraint_type}=\"{constraint['constant']}dp\"",
            f"      app:layout_constraint{constraint_type}_to{related_constraint_type}Of=\"{related_view}\""
        ]
        return lines

    def height_constraint_lines(self, constraint):
        self.height = constraint['constant']
        return [f"      android:layout_height=\"{self.height}dp\""]

    def width_constraint_lines(self, constraint):
        self.width = constraint['constant']
        return [f"      android:layout_width=\"{self.width}dp\""]

    def top_constraint_lines(self, constraint):
        return self.standard_constraint_lines(constraint)

    def bottom_constraint_lines(self, constraint):
        return self.standard_constraint_lines(constraint)

    def leading_constraint_lines(self, constraint):
        return self.standard_constraint_lines(constraint)

    def trailing_constraint_lines(self, constraint):
        return self.standard_constraint_lines(constraint)  

    def center_x_constraint_lines(self, constraint):
        lines = []
        lines += self.leading_constraint_lines({'type': 'leading', 'constant': '0', 'related_view': 'parent', 'related_constraint': 'leading'})
        lines += self.trailing_constraint_lines({'type': 'trailing', 'constant': '0', 'related_view': 'parent', 'related_constraint': 'trailing'})
        return lines

    def build(self):
        print("Building...")