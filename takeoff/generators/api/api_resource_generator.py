import os
from jinja2 import Template
from .api_base_generator import ApiBaseGenerator
from pathlib import Path

class ApiResourceGenerator(ApiBaseGenerator):
    def __init__(self, name, options):
        super().__init__(name, options)
        self.model_name = ''
        self.model_attributes = []

    def model_class_name(self):
        return self.camelize(self.model_name)

    def run(self):
        self.model_name = self.options.pop(0)
        print(f"Running Api Resource Generator: {self.name} : {self.model_name}")
        self.load_model_attributes()
        self.prepare_urls()
        self.prepare_serializer()
        self.prepare_resource_view()

    def writeable_attributes(self):
        atts = []
        locked_fields = ['created_at', 'updated_at']

        for attribute in self.model_attributes:
            if attribute['attribute_name'] not in locked_fields:
                atts.append(attribute)

        return atts

    def load_model_attributes(self):
        model_file = f"{self.project_folder()}/api/models/{self.model_name}.py"
        lines = list(open(model_file, 'r'))

        django_field_types = [
            'models.CharField',
            'models.TextField',
            'models.DateTimeField',
            'models.IntegerField',
            'models.BooleanField',
            'models.FloatField',
            'models.ForeignKey',
        ]

        for line in lines:
            print(line)
            for field_type in django_field_types:
                if f"= {field_type}" in line:
                    attribute_name = line.strip().split("=")[0].strip()
                    attribute_type = line.strip().split("=")[1].strip().split("(")[0].strip()
                    if attribute_type == 'models.ForeignKey':
                        attribute_name = f"{attribute_name}_id"
                        attribute_type = "models.IntegerField"
                    attribute_definition = { 
                        'attribute_name': attribute_name, 
                        'attribute_type': attribute_type,
                        'attribute_class': attribute_type.replace('models.', '')
                    }
                    self.model_attributes.append(attribute_definition)

    def prepare_urls(self):
        destination = f"dist/{self.name}/api/{self.name}/api/urls.py"
        import_line = "from django.urls import include, path"
        self.add_line_after_pattern(destination, f"{import_line}\n", "from django.conf.urls import include, url")
        router_line = "router = routers.DefaultRouter()"
        self.add_line_after_pattern(destination, f"{router_line}\n", "app_name = 'api'")
        resource_line = f"router.register(r'{self.pluralize(self.model_name)}', views.{self.camelize(self.model_name)}ViewSet)\n"
        self.add_line_after_pattern(destination, resource_line, router_line)
        self.add_line_after_pattern(destination, "    path('', include(router.urls)),\n", "urlpatterns = [")

    def prepare_serializer(self):
        template_path = f"{self.templates_path}/serializer.template"
        destination_folder = f"{self.project_folder()}/api/serializers"
        os.system(f"mkdir -p {destination_folder}")
        Path(f"{destination_folder}/__init__.py").touch()
        destination = f"{destination_folder}/{self.model_name}_serializer.py"

        with open(template_path) as f:
            template_contents = f.read()

        template = Template(template_contents)
        contents = template.render(generator=self)

        with open(destination, 'w') as f:
            f.write(contents)

    def prepare_resource_view(self):
        template_path = f"{self.templates_path}/resource_view.template"
        destination_folder = f"{self.project_folder()}/api/views"
        os.system(f"mkdir -p {destination_folder}")
        Path(f"{destination_folder}/__init__.py").touch()
        destination = f"{destination_folder}/{self.model_name}.py"

        with open(template_path) as f:
            template_contents = f.read()

        template = Template(template_contents)
        contents = template.render(generator=self)

        with open(destination, 'w') as f:
            f.write(contents)

        destination = f"{self.project_folder()}/api/views/__init__.py"
        self.add_line_after_pattern(destination, f"from .{self.model_name} import *\n", "from .main import")

    def fields_list(self):
        fields = list(map(lambda x: f"'{x['attribute_name']}'", self.writeable_attributes()))
        fields = ", ".join(fields)
        return f"[{fields}]"