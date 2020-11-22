import re
import os
from jinja2 import Template

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class GeneratorBase:

    def __init__(self, name, options):
        self.name = name
        self.options = options
        self.python = 'python3'
        self.pip = 'pip3'
        self.templates_path = os.path.join(BASE_DIR, 'templates')

    def setup(self):
        print(f"Setting up: {type(self).__name__}")
    
    def base_dist_folder(self):
        return 'dist'        

    def project_type(self):
        return 'undefined'

    def project_folder(self):
        return f"{self.base_dist_folder()}/{self.name}/{self.project_type()}/{self.name}"
    
    def titleize(self, string):
        return string.replace('_', ' ').title()

    def camelize(self, string):
        return self.titleize(string).replace(' ', '')
    
    def pluralize(self, string):
        if re.match(r'(.*)y$', string):
            return re.sub(r'y$', 'ies', string)
        elif re.match(r'(.*)s$', string):
            return string

        return f"{string}s"

    def system_call(self, command):
        os.system(command)

    def line_at_pattern(self, pattern, lines):
        finish = 0

        for index, line in enumerate(lines):
            if pattern in line:
                finish = index

        return finish
    
    def render_template(self, template_path, destination, overwrite=False):
        if os.path.exists(destination) and not overwrite:
            return
        
        with open(template_path) as f:
            template_contents = f.read()

        template = Template(template_contents)
        contents = template.render(generator=self)
        with open(destination, 'w') as f:
            f.write(contents)

    def add_line_before_pattern(self, destination, new_line, pattern, force=False):
        lines = list(open(destination, 'r'))
        last_line = self.line_at_pattern(pattern, lines)

        if new_line not in lines or force:
            lines.insert(last_line, new_line)
            last_line += 1

        with open(destination, 'w') as file:
            file.writelines(lines)

    def add_line_after_pattern(self, destination, new_line, pattern):
        lines = list(open(destination, 'r'))
        last_line = self.line_at_pattern(pattern, lines)

        if new_line not in lines:
            lines.insert(last_line + 1, new_line)
            last_line += 1

        with open(destination, 'w') as file:
            file.writelines(lines)

    def add_lines_before_last_line(self, destination, new_lines, identifier=''):
        lines = list(open(destination, 'r'))

        if identifier != '':
            for line in lines:
                if identifier in line:
                    return

        for new_line in new_lines:
            lines.insert(len(lines) - 1, f"{new_line}\n")

        with open(destination, 'w') as file:
            file.writelines(lines)
    
    def replace_lines_for_block(self, destination, first_pattern, block_start_pattern, block_end_pattern, new_lines):
        new_lines = list(map(lambda x: f"{x}\n", new_lines.split("\n")))
        lines = list(open(destination, 'r'))
        within_subblock = False
        
        # Pattern check: dont do a second pass
        if new_lines[0] in lines:
            return

        before_lines = []
        after_lines = []
        started = False
        finished = False

        for line in lines:
            if started and block_end_pattern in line:
                if within_subblock:
                    within_subblock = False
                else:
                    finished = True

            if started and block_start_pattern in line:
                within_subblock = True

            if not started:
                before_lines.append(line)
            elif started and finished:
                after_lines.append(line)

            if first_pattern in line:
                started = True

        all_lines = before_lines + new_lines + after_lines

        with open(destination, 'w') as file:
            file.writelines(all_lines)

    def append_lines_to_block(self, destination, first_pattern, block_start_pattern, block_end_pattern, new_lines):
        new_lines = list(map(lambda x: f"{x}\n", new_lines.split("\n")))
        lines = list(open(destination, 'r'))
        within_subblock = False
        
        # Pattern check: dont do a second pass
        if new_lines[0] in lines:
            return

        before_lines = []
        after_lines = []
        started = False
        finished = False

        for line in lines:            
            if started and block_end_pattern in line:
                if within_subblock:
                    within_subblock = False
                else:
                    finished = True

            if started and block_start_pattern in line:
                within_subblock = True

            if not started:
                before_lines.append(line)
            elif started and not finished:
                before_lines.append(line)
            elif started and finished:
                after_lines.append(line)

            if first_pattern in line:
                started = True

        all_lines = before_lines + new_lines + after_lines

        with open(destination, 'w') as file:
            file.writelines(all_lines)