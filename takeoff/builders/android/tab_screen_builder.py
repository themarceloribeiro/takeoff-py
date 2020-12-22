import os
from .android_component_builder import AndroidComponentBuilder

class TabScreenBuilder(AndroidComponentBuilder):
    def build(self):
        self.icon = None
        self.icon_file = None
        self.load_attributes()
        self.load_icon_name()
        self.copy_icon()
        self.write_fragment_class()
        self.write_fragment_layout()
        self.write_tab_item()
        self.add_nav_item()
        self.add_activity_connector()
        print("Finished Building tab screen")        
    
    def copy_icon(self):
        if self.icon:
            destination_folder = f"{self.generator.project_folder()}/app/src/main/res/drawable"
            os.system(f"cp {self.icon} {destination_folder}/{self.icon_file}")
            os.system(f"cp {self.icon} {destination_folder}/{self.icon_file.replace('.', '_off.')}")

    def load_icon_name(self):
        if self.icon:
            self.icon_file = self.icon.split('/')[-1]
            self.icon_name = self.icon_file.split('.')[0]
        else:
            self.icon_name = 'unknown'

    def write_fragment_class(self):
        package_path = self.generator.android_prefix.replace('.', '/')
        template_path = f"{self.generator.templates_path}/app/src/main/java/screen_fragment.kt.template"
        destination_folder = f"{self.generator.project_folder()}/app/src/main/java/{package_path}/{self.name.lower()}"
        os.system(f"mkdir -p {destination_folder}")
        destination = f"{destination_folder}/{self.generator.camelize(self.name)}Fragment.kt"
        self.write_from_template(template_path, destination)

    def write_fragment_layout(self):
        package_path = self.generator.android_prefix.replace('.', '/')
        template_path = f"{self.generator.templates_path}/app/src/main/res/layout/screen_fragment.xml.template"
        destination_folder = f"{self.generator.project_folder()}/app/src/main/res/layout"
        os.system(f"mkdir -p {destination_folder}")
        destination = f"{destination_folder}/{self.name.lower()}_fragment.xml"
        self.write_from_template(template_path, destination)
    
    def write_tab_item(self):
        package_path = self.generator.android_prefix.replace('.', '/')
        template_path = f"{self.generator.templates_path}/app/src/main/res/drawable/screen_item_tab.xml.template"
        destination_folder = f"{self.generator.project_folder()}/app/src/main/res/drawable"
        os.system(f"mkdir -p {destination_folder}")
        destination = f"{destination_folder}/{self.name.lower()}_item.xml"
        self.write_from_template(template_path, destination)
    
    def add_nav_item(self):
        lines = [
            f"    <!-- {self.name} menu item -->",
            "    <item",
            f"        android:id=\"@+id/menu{self.generator.camelize(self.name)}\"",
            f"        android:title=\"{self.generator.camelize(self.name)}\"",
            f"        android:icon=\"@drawable/{self.name.lower()}_item\"",
            "        app:showAsAction=\"always\"",
            "    />"
        ]
        
        destination_folder = f"{self.generator.project_folder()}/app/src/main/res/menu"
        destination = f"{destination_folder}/nav_items.xml"
        identifier = lines[0]
        self.generator.add_lines_before_last_line(destination, lines, identifier)
    
    def add_activity_connector(self):
        lines = [ 
            f"            R.id.menu{self.generator.camelize(self.name)} -> show{self.generator.camelize(self.name)}()"
        ]
        destination_folder = f"{self.generator.project_folder()}/app/src/main/java/{self.generator.android_prefix.replace('.', '/')}/home"
        destination = f"{destination_folder}/HomeActivity.kt"
        self.generator.append_lines_to_block(destination, 'when(item.itemId) {', 'when(item.itemId) {', '}', "\n".join(lines))

        method = "\n".join([
            f"    fun show{self.generator.camelize(self.name)}() {'{'}",
            f"        showFragment({self.generator.camelize(self.name)}Fragment())",
            "    }"
        ])
        self.generator.add_method_to_class('home/HomeActivity.kt', method, f"show{self.generator.camelize(self.name)}")
        self.generator.add_import_line(destination, f"com.welcomehero.app.{self.name.lower()}.{self.generator.camelize(self.name)}Fragment")