import os
from jinja2 import Template
from ..generator_base import GeneratorBase
from pathlib import Path

class WebResourceGenerator(GeneratorBase):
    def __init__(self, name, options):
        super().__init__(name, options)
        self.model_name = ''

    def project_type(self):
        return 'web'

    def model_class_name(self):
        return self.camelize(self.model_name)

    def run(self):
        self.model_name = self.options.pop(0)
        print(f"Running Web Resource Generator: {self.name} : {self.model_name}")

        self.write_view_file()
        self.update_views_file()
        self.write_views()
        self.prepare_urls()

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

    def update_views_file(self):
        current_file = f"{self.project_folder()}/main/views/__init__.py"

        lines = list(open(current_file, 'r'))
        line = f"from .{self.pluralize(self.model_name)} import *\n"
        
        if line not in lines:
            lines.append(line)
        
        with open(current_file, 'w') as file:
            file.writelines(lines)
    
    def write_views(self):
        template_path = f"{self.templates_path}/web/views/index.html.template"
        destination_folder = f"{self.project_folder()}/main/templates/{self.pluralize(self.model_name)}"
        os.system(f"mkdir -p {destination_folder}")
        destination = f"{destination_folder}/index.html"

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

        line = f"    path('{self.pluralize(self.model_name)}/', views.{self.pluralize(self.model_name)}.index, name='{self.pluralize(self.model_name)}'),\n"

        if line not in lines:
            last_line = self.urls_last_line(lines)
            lines.insert(last_line, line)

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