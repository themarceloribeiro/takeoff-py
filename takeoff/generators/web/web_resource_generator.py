import os
from jinja2 import Template
from ..generator_base import GeneratorBase
from pathlib import Path

class WebResourceGenerator(GeneratorBase):
    def __init__(self, name, options):
        super().__init__(name, options)
        self.model_name = ''
        self.model_attributes = []

    def project_type(self):
        return 'web'

    def model_class_name(self):
        return self.camelize(self.model_name)

    def run(self):
        self.model_name = self.options.pop(0)
        print(f"Running Web Resource Generator: {self.name} : {self.model_name}")

        self.load_model_attributes()
        self.write_view_file()
        self.update_views_file()
        self.write_form_file()
        self.write_views()
        self.prepare_urls()

    def writeable_attributes(self):
        atts = []
        locked_fields = ['created_at', 'updated_at']

        for attribute in self.model_attributes:
            if attribute['attribute_name'] not in locked_fields:
                atts.append(attribute)

        return atts

    def load_model_attributes(self):
        model_file = f"{self.project_folder()}/main/models/{self.model_name}.py"
        lines = list(open(model_file, 'r'))

        django_field_types = [
            'models.CharField',
            'models.TextField',
            'models.DateTimeField',
            'models.IntegerField',
            'models.BooleanField',
            'models.FloatField'
        ]

        for line in lines:
            for field_type in django_field_types:
                if f"= {field_type}" in line:
                    attribute_name = line.strip().split("=")[0].strip()
                    attribute_type = line.strip().split("=")[1].strip().split("(")[0].strip()
                    self.model_attributes.append({ 'attribute_name': attribute_name, 'attribute_type': attribute_type })

    def write_view_file(self):
        template_path = f"{self.templates_path}/web/view.template"
        destination_folder = f"{self.project_folder()}/main/views"
        os.system(f"mkdir -p {destination_folder}")
        Path(f"{destination_folder}/__init__.py").touch()
        destination = f"{destination_folder}/{self.pluralize(self.model_name)}.py"

        with open(template_path) as f:
            template_contents = f.read()

        template = Template(template_contents)
        contents = template.render(generator=self)

        with open(destination, 'w') as f:
            f.write(contents)

    def write_form_file(self):
        template_path = f"{self.templates_path}/web/form.template"
        destination_folder = f"{self.project_folder()}/main/forms"
        os.system(f"mkdir -p {destination_folder}")
        Path(f"{destination_folder}/__init__.py").touch()
        destination = f"{destination_folder}/{self.model_name}.py"

        with open(template_path) as f:
            template_contents = f.read()

        template = Template(template_contents)
        contents = template.render(generator=self)

        with open(destination, 'w') as f:
            f.write(contents)

    def update_views_file(self):
        current_file = f"{self.project_folder()}/main/views/__init__.py"

        lines = list(open(current_file, 'r'))
        line = f"from .{self.pluralize(self.model_name)} import *\n"

        if line not in lines:
            lines.append(line)
        
        with open(current_file, 'w') as file:
            file.writelines(lines)
    
    def write_views(self):
        views = ['index', 'show', 'new', 'edit']
        for view in views:
            self.render_view_template(view)
    
    def render_view_template(self, view):
        template_path = f"{self.templates_path}/web/views/{view}.html.template"
        destination_folder = f"{self.project_folder()}/main/templates/{self.pluralize(self.model_name)}"
        os.system(f"mkdir -p {destination_folder}")
        destination = f"{destination_folder}/{view}.html"

        with open(template_path) as f:
            template_contents = f.read()

        template = Template(template_contents)
        contents = template.render(generator=self)
        
        with open(destination, 'w') as f:
            f.write(contents)

    def prepare_urls(self):
        urls_file = f"dist/{self.name}/web/{self.name}/main/urls.py"
        lines = list(open(urls_file, 'r'))

        for index, line in enumerate(lines):
            if line == "from django.urls import path\n":
                lines[index] = line.replace('path', 'path, include')

        new_lines = [
            f"path('{self.pluralize(self.model_name)}/', views.{self.pluralize(self.model_name)}.index, name='{self.pluralize(self.model_name)}')",
            f"path('{self.pluralize(self.model_name)}/new', views.{self.pluralize(self.model_name)}.new, name='new_{self.model_name}')",
            f"path('{self.pluralize(self.model_name)}/<int:{self.model_name}_id>', views.{self.pluralize(self.model_name)}.show, name='{self.model_name}')",
            f"path('{self.pluralize(self.model_name)}/<int:{self.model_name}_id>/edit', views.{self.pluralize(self.model_name)}.edit, name='edit_{self.model_name}')",
            f"path('{self.pluralize(self.model_name)}/<int:{self.model_name}_id>/delete', views.{self.pluralize(self.model_name)}.delete, name='delete_{self.model_name}')",
        ]
    
        last_line = self.urls_last_line(lines)

        for new_line in new_lines:
            new_line = f"    {new_line},\n"
            if new_line not in lines:
                lines.insert(last_line, new_line)
                last_line += 1

        with open(urls_file, 'w') as file:
            file.writelines(lines)

    def urls_last_line(self, lines):
        started = False
        finish = 0

        for index, line in enumerate(lines):
            if 'urlpatterns' in line:
                started = True
            if started and finish == 0 and ']' in line:
                finish = index

        return finish
    
    def fields_list(self):
        fields = list(map(lambda x: f"'{x['attribute_name']}'", self.writeable_attributes()))
        fields = ", ".join(fields)
        return f"[{fields}]"
    
    def labels_list(self):
        fields = list(map(lambda x: f"'{x['attribute_name']}': '{self.titleize(x['attribute_name'])}'", self.writeable_attributes()))
        fields = ", ".join(fields)
        return '{' + f"{fields}" + '}'