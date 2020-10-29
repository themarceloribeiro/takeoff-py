from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch
from takeoff import *
import os

class WebModelGeneratorTest(TestCase):

    def setUp(self):
        os.system('rm -rf test_dist/blog')
        self.project_generator = WebProjectGenerator('blog', [])
        self.project_generator.base_dist_folder = MagicMock(return_value='test_dist')
        self.g = WebModelGenerator('blog', ['category', 'name:string', 'summary:text'])
        self.g.base_dist_folder = MagicMock(return_value='test_dist')

    def setup_project(self):
        self.project_generator.system_call = self.real_system_call
        self.project_generator.create_structure_folders()
        self.project_generator.create_django_project()
        self.project_generator.prepare_settings()

    def test_project_folder(self):
        self.g.load_attributes()
        self.assertEqual(self.g.name, 'blog')
        expected_attributes = [
            {'class': 'CharField', 'field_extra': "default='', max_length=250", 'name': 'name', 'type': 'string'},
            {'class': 'TextField', 'field_extra': "default=''", 'name': 'summary', 'type': 'text'},
            {'class': 'DateTimeField', 'field_extra': 'auto_now_add=True', 'name': 'created_at', 'type': 'datetime'},
            {'class': 'DateTimeField', 'field_extra': 'auto_now_add=True', 'name': 'updated_at', 'type': 'datetime'}
        ]
        self.assertEqual(self.g.model_attributes, expected_attributes)

    def test_attribute_class(self):
        self.assertEqual(self.g.attribute_class('string'), 'CharField')
        self.assertEqual(self.g.attribute_class('text'), 'TextField')
        self.assertEqual(self.g.attribute_class('integer'), 'IntegerField')
        self.assertEqual(self.g.attribute_class('float'), 'FloatField')
        self.assertEqual(self.g.attribute_class('boolean'), 'BooleanField')
        self.assertEqual(self.g.attribute_class('belongs_to'), 'ForeignKey')

    def test_attribute_field_extra(self):
        self.assertEqual(self.g.attribute_field_extra('string'), "default='', max_length=250")
        self.assertEqual(self.g.attribute_field_extra('text'), "default=''")
        self.assertEqual(self.g.attribute_field_extra('integer'), 'default=0')
        self.assertEqual(self.g.attribute_field_extra('float'), 'default=0.0')
        self.assertEqual(self.g.attribute_field_extra('boolean'), 'default=False')
        self.assertEqual(self.g.attribute_field_extra('belongs_to', 'Category'), 'Category, on_delete=models.CASCADE,  null=True')
    
    def test_write_model_file(self):
        self.g.write_model_file()
        file_path = f"{self.g.project_folder()}/main/models/{self.g.model_name}.py"
        lines = list(open(file_path, 'r'))
        print(lines)