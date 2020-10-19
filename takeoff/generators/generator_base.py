class GeneratorBase:
    def __init__(self, name, options):
        self.name = name
        self.options = options
        self.python = 'python3'
        self.templates_path = '/Users/marcelo/work/takeoff/python/takeoff/takeoff/templates'

    def setup(self):
        print(f"Setting up: {type(self).__name__}")

    def project_type(self):
        return 'undefined'

    def project_folder(self):
        return f"dist/{self.name}/{self.project_type()}/{self.name}"