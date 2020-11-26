import os
from jinja2 import Template
from .api_base_generator import ApiBaseGenerator
from pathlib import Path

class ApiAuthenticationGenerator(ApiBaseGenerator):
    def __init__(self, name, options):
        super().__init__(name, options)

    def run(self):
        print(f"Running API Authentication Generator: {self.name}")
        self.setup()
        self.install_required_libraries()
        self.set_rest_auth_settings()
        self.set_urls()
        self.render_templates()

    def required_libraries(self):
        return [
            'djangorestframework-jwt',
        ]
    
    def set_rest_auth_settings(self):
        lines = ("\n").join([
            "    'DEFAULT_PERMISSION_CLASSES': (",
            "        'rest_framework.permissions.IsAuthenticated',",
            "    ),",
            "    'DEFAULT_AUTHENTICATION_CLASSES': (",
            "        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',",
            "        'rest_framework.authentication.SessionAuthentication',",
            "        'rest_framework.authentication.BasicAuthentication',",
            "    ),",
        ])

        destination = f"{self.project_folder()}/{self.name}/settings.py"
        self.append_lines_to_block(destination, 'DEFAULT_PERMISSION_CLASSES', 'REST_FRAMEWORK', '}', lines)

        jwt_lines = [
            "JWT_AUTH = {",
            "    'JWT_ALLOW_REFRESH': True,",
            "    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),",
            "    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=30),",
            "}",
        ]

        self.add_lines(destination, jwt_lines)
        self.add_line_after_pattern(destination, 'import datetime', 'from pathlib import Path')
    
    def set_urls(self):
        destination = f"{self.base_dist_folder()}/{self.name}/api/{self.name}/{self.name}/urls.py"
        self.add_url_line('tokens/refresh', 'refresh_jwt_token')
        self.add_url_line('tokens', 'obtain_jwt_token')
        self.add_line_after_pattern(destination, "from django.conf.urls import include, url\n", 'from django.urls import path, include')
        self.add_line_after_pattern(destination, "from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token\n", 'from django.urls import path, include')

        destination = f"{self.base_dist_folder()}/{self.name}/api/{self.name}/api/urls.py"
        self.add_line_after_pattern(destination, "from django.urls import path\n", 'from .main import *')
        self.add_line_after_pattern(destination, "    path('me/', views.user),\n", 'urlpatterns')
        
        destination = f"{self.base_dist_folder()}/{self.name}/api/{self.name}/api/views/__init__.py"
        self.add_line_after_pattern(destination, "from .user import *\n", 'from .main import *')
    
    def render_templates(self):
        template_path = f"{self.templates_path}/user_view.template"
        destination = f"{self.project_folder()}/api/views/user.py"
        self.render_template(template_path, destination)

        destination_folder = f"{self.project_folder()}/api/serializers"
        os.system(f"mkdir -p {destination_folder}")
        template_path = f"{self.templates_path}/user_serializer.template"
        destination = f"{destination_folder}/user_serializer.py"
        self.render_template(template_path, destination)