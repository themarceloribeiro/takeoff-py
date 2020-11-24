import os
from jinja2 import Template
from .api_base_generator import ApiBaseGenerator
from pathlib import Path

class ApiProjectGenerator(ApiBaseGenerator):
    def __init__(self, name, options):
        self.django_admin = os.getenv('PYTHON_DJANGO_ADMIN', 'django-admin')
        super().__init__(name, options)

    def run(self):
        print(f"Running API Project Generator: {self.name}")
        self.setup()
        self.install_required_libraries()
        self.create_structure_folders()
        self.create_django_project()
        self.prepare_settings()
        self.create_main_view()        
        self.prepare_urls()
        self.migrate()
        self.create_admin()
    
    def migrate(self):
        self.system_call(f"cd {self.project_folder()} && {self.python} manage.py migrate")

    def install_required_libraries(self):
        libs = ['django', 'djangorestframework']
        for lib in libs:
            self.system_call(f"{self.pip} install {lib}")

    def start_django_project(self):
        self.system_call(f"cd {self.base_dist_folder()}/{self.name}/api && {self.django_admin} startproject {self.name}")

    def start_api_app(self):
        self.system_call(f"cd {self.base_dist_folder()}/{self.name}/api/{self.name} && {self.python} manage.py startapp api")

    def create_django_project(self):
        print('Creating Django API Project')
        self.start_django_project()
        self.start_api_app()

    def create_structure_folders(self):
        fullpath = f"{self.base_dist_folder()}/{self.name}/api/"
        print(f"    Creating API Folder: {fullpath}")
        self.system_call(f"mkdir -p {fullpath}")

    def create_admin(self):
        self.system_call(f"cd {self.project_folder()} && {self.python} manage.py createsuperuser")

    def prepare_settings(self):
        self.add_app('api')
        self.add_app('rest_framework')

        settings_lines = [
            "REST_FRAMEWORK = {",
            "    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',",
            "    'PAGE_SIZE': 10",
            "}",
        ]

        destination = f"{self.base_dist_folder()}/{self.name}/api/{self.name}/{self.name}/settings.py"
        self.add_lines(destination, settings_lines)

    def generate_api_urls(self):
        template_path = f"{self.templates_path}/urls.template"
        destination = f"{self.base_dist_folder()}/{self.name}/api/{self.name}/api/urls.py"

        with open(template_path) as f:
            template_contents = f.read()

        template = Template(template_contents)
        contents = template.render(generator=self, app_name='api')
        
        with open(destination, 'w') as f:
            f.write(contents)

    def prepare_urls(self):
        self.generate_api_urls()
        self.add_app_url_pattern('api', '')
    
    def create_main_view(self):
        views_folder = f"{self.base_dist_folder()}/{self.name}/api/{self.name}/api/views"
        self.system_call(f"mkdir -p {views_folder}")
        
        destination = f"{views_folder}/__init__.py"
        self.system_call(f"touch {destination}")
        lines = ["from .main import *"]
        self.add_lines(destination, lines)

        self.render_template(f"{self.templates_path}/main_view.template", f"{views_folder}/main.py")