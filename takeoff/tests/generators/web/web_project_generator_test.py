from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch
from takeoff import *
import os

class WebProjectGeneratorTest(TestCase):

    def setUp(self):
        os.system('rm -rf test_dist/blog')
        self.g = WebProjectGenerator('blog', [])
        self.real_system_call = self.g.system_call
        self.g.system_call = MagicMock()
        self.g.base_dist_folder = MagicMock(return_value='test_dist')
    
    def setup_project(self):
        self.g.system_call = self.real_system_call
        self.g.create_structure_folders()
        self.g.create_django_project()
        self.g.prepare_settings()
    
    def line_block(self, starting_line, finishing_line, lines):
        block = []
        started = False
        for line in lines:
            if line == starting_line:
                started = True
            if started:
                block.append(line)
                if line == finishing_line:
                    started = False
        
        return block

    def test_project_folder(self):
        self.assertEqual(self.g.project_folder(), 'test_dist/blog/web/blog')
    
    def test_create_structure_folders(self):
        self.g.create_structure_folders()
        self.g.system_call.assert_called_with('mkdir -p test_dist/blog/web/')

    def test_migrate_call(self):
        self.g.migrate()
        self.g.system_call.assert_called_with('cd test_dist/blog/web/blog && python3 manage.py migrate')

    def test_install_libraries_call(self):
        self.g.install_required_libraries()
        self.g.system_call.assert_called_with('pip3 install django-bootstrap4')
    
    def test_start_django_project(self):
        self.g.start_django_project()
        self.g.system_call.assert_called_with('cd test_dist/blog/web && django-admin startproject blog')

    def test_start_main_app(self):
        self.g.start_main_app()
        self.g.system_call.assert_called_with('cd test_dist/blog/web/blog && python3 manage.py startapp main')
    
    def test_create_admin(self):
        self.g.create_admin()
        self.g.system_call.assert_called_with('cd test_dist/blog/web/blog && python3 manage.py createsuperuser')
    
    def test_prepare_settings(self):
        self.setup_project()
        file = open('test_dist/blog/web/blog/blog/settings.py', 'r')
        lines = list(file)
        file.close()
        self.assertIn("    'main',\n", lines)
        self.assertIn("    'bootstrap4',\n", lines)

    def test_generate_main_urls(self):
        self.setup_project()
        self.g.generate_main_urls()
        file = open('test_dist/blog/web/blog/main/urls.py', 'r')
        lines = list(file)
        file.close()

        expected_lines = [
            'from django.urls import path\n', 
            'from . import views\n', 
            "app_name = 'main'\n", 
            '\n', 
            'urlpatterns = [\n', ']'
        ]        
        self.assertEqual(expected_lines, lines)
    
    def test_prepare_urls(self):
        self.setup_project()
        self.g.prepare_urls()
        file = open('test_dist/blog/web/blog/blog/urls.py', 'r')
        lines = self.line_block(
            'urlpatterns = [\n',
            ']\n',
            list(file)
        )
        file.close()
        expected_lines = [
            'urlpatterns = [\n',
            "    path('', include('main.urls')),\n",
            "    path('admin/', admin.site.urls),\n",
            ']\n'
        ]
        self.assertEqual(expected_lines, lines)