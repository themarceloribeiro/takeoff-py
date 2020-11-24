import os
from jinja2 import Template
from ..base_generator import BaseGenerator
from pathlib import Path

class ApiBaseGenerator(BaseGenerator):
    def __init__(self, name, options):
        super().__init__(name, options)
        self.templates_path = f"{self.templates_path}/api"

    def project_type(self):
        return 'api'

    def add_app(self, app_name):
        settings_file = f"{self.base_dist_folder()}/{self.name}/api/{self.name}/{self.name}/settings.py"
        file = open(settings_file, 'r')
        lines = list(file)
        file.close()
        last_line = self.installed_apps_last_line(lines)
        lines.insert(last_line, f"    '{app_name}',\n")

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

    def add_app_url_pattern(self, app_name, pattern):
        urls_file = f"{self.base_dist_folder()}/{self.name}/api/{self.name}/{self.name}/urls.py"
        file = open(urls_file, 'r')
        lines = list(file)
        file.close()

        for index, line in enumerate(lines):
            if line == "from django.urls import path\n":
                lines[index] = line.replace('path', 'path, include')

        line = f"    path('{pattern}', include('{app_name}.urls')),\n"

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