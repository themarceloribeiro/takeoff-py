from unittest import TestCase
from takeoff import *

class GeneratorTest(TestCase):

    def setUp(self):
        self.g = Generator(['web:project', 'blog'])

    def test_load_type_subtype(self):
        self.assertEqual(self.g.generator_type, 'web')
        self.assertEqual(self.g.generator_subtype, 'project')
    
    def test_load_name(self):
        self.assertEqual(self.g.name, 'blog')
    
    def test_return_generator_class(self):
        self.assertEqual(type(self.g.get_generator()).__name__, 'WebGenerator')
        