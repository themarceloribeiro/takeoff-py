from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch
from takeoff import *

class WebProjectGeneratorTest(TestCase):

    def setUp(self):
        self.g = WebProjectGenerator('blog', [])
        self.real_system_call = self.g.system_call
        self.g.system_call = MagicMock()

    def test_project_folder(self):
        self.assertEqual(self.g.project_folder(), 'dist/blog/web/blog')
    
    def test_create_structure_folders(self):
        self.g.create_structure_folders()
        self.g.system_call.assert_called_with('mkdir -p dist/blog/web/')

    def test_migrate_call(self):
        self.g.migrate()
        self.g.system_call.assert_called_with('cd dist/blog/web/blog && python3 manage.py migrate')

    def test_install_libraries_call(self):
        self.g.install_required_libraries()
        self.g.system_call.assert_called_with('pip3 install django-bootstrap4')
    
    def test_start_django_project(self):
        self.g.start_django_project()
        self.g.system_call.assert_called_with('cd dist/blog/web && django-admin startproject blog')

    def test_start_main_app(self):
        self.g.start_main_app()
        self.g.system_call.assert_called_with('cd dist/blog/web/blog && python3 manage.py startapp main')
    
    def test_create_admin(self):
        self.g.create_admin()
        self.g.system_call.assert_called_with('cd dist/blog/web/blog && python3 manage.py createsuperuser')
    
    def test_prepare_settings(self):
        self.g.system_call = self.real_system_call
        self.g.create_django_project()
        self.g.prepare_settings()