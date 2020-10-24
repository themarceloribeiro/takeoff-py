import os
from jinja2 import Template
from ..generator_base import GeneratorBase
from pathlib import Path

class WebProjectGenerator(GeneratorBase):
    def __init__(self, name, options):
        super().__init__(name, options)

    def project_type(self):
        return 'web'

    def run(self):
        print(f"Running Web Project Generator: {self.name}")        
        self.setup()
        self.install_required_libraries()
        self.create_structure_folders()
        self.create_django_project()
        self.prepare_settings()
        self.prepare_urls()
        self.migrate()
        self.create_admin()
    
    def migrate(self):
        os.system(f"cd {self.project_folder()} && {self.python} manage.py migrate")

    def install_required_libraries(self):
        libs = ['django-bootstrap4']
        for lib in libs:
            os.system(f"{self.pip} install {lib}")

    def create_django_project(self):
        print('Creating Django Project')
        os.system(f"cd dist/{self.name}/web && django-admin startproject {self.name}")
        os.system(f"cd dist/{self.name}/web/{self.name} && {self.python} manage.py startapp main")

    def create_structure_folders(self):
        fullpath = f"dist/{self.name}/web/"
        print(f"    Creating Web Folder: {fullpath}")
        os.system(f"mkdir -p {fullpath}")
    
    def prepare_settings(self):
        settings_file = f"dist/{self.name}/web/{self.name}/{self.name}/settings.py"
        lines = list(open(settings_file, 'r'))
        last_line = self.installed_apps_last_line(lines)
        lines.insert(last_line - 1, "    'main',\n")
        lines.insert(last_line - 1, "    'bootstrap4',\n")
        
        with open(settings_file, 'w') as file:
            file.writelines(lines)

    def installed_apps_last_line(self, lines):
        started = False
        finish = 0

        for index, line in enumerate(lines):
            if 'INSTALLED_APPS' in line:
                started = True
            if started > 0 and finish == 0 and ']' in line:
                finish = index

        return finish

    def generate_main_urls(self):
        template_path = f"{self.templates_path}/web/urls.template"
        destination = f"dist/{self.name}/web/{self.name}/main/urls.py"

        with open(template_path) as f:
            template_contents = f.read()

        template = Template(template_contents)
        contents = template.render(generator=self, app_name='main')
        
        with open(destination, 'w') as f:
            f.write(contents)

    def prepare_urls(self):
        self.generate_main_urls()
        urls_file = f"dist/{self.name}/web/{self.name}/{self.name}/urls.py"
        lines = list(open(urls_file, 'r'))

        for index, line in enumerate(lines):
            if line == "from django.urls import path\n":
                lines[index] = line.replace('path', 'path, include')

        line = f"    path('', include('main.urls')),\n"
        
        if line not in lines:
            last_line = self.urls_last_line(lines)
            lines.insert(last_line - 1, line)

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

    def create_admin(self):
        os.system(f"cd {self.project_folder()} && {self.python} manage.py createsuperuser")