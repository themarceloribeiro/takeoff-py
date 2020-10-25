import os
from jinja2 import Template
from .web_base_generator import WebBaseGenerator
from pathlib import Path

class WebProjectGenerator(WebBaseGenerator):
    def __init__(self, name, options):
        super().__init__(name, options)

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
        self.add_app('main')
        self.add_app('bootstrap4')
        self.add_setting('LOGIN_REDIRECT_URL', '/')
        self.add_setting('LOGOUT_REDIRECT_URL', '/')

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
        self.add_app_url_pattern('main', '')

    def create_admin(self):
        os.system(f"cd {self.project_folder()} && {self.python} manage.py createsuperuser")