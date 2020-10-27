from unittest import TestCase
from takeoff import *

class WebGeneratorTest(TestCase):

    def setUp(self):
        self.g = WebGenerator('blog', 'project', [])

    def test_return_generator_class(self):
        self.assertEqual(type(self.g.generator()).__name__, 'WebProjectGenerator')
        