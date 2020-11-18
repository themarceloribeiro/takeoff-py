import os
from jinja2 import Template
from .android_base_generator import AndroidBaseGenerator
from pathlib import Path
from shutil import copyfile

class AndroidProjectGenerator(AndroidBaseGenerator):

    def run(self):
        self.setup()
        print(f">>> Running Android Project Generator: {self.name}")
        self.create_structure_folders()
        self.create_structure_files()

    def create_structure_folders(self):
        print(f">>> Creating directory structure: {self.android_prefix}.{self.name}")

        for folder in self.main_project_folders():
            fullpath = f"{self.project_folder()}/{folder}"
            print(f"    Creating Android Folder: {fullpath}")
            os.system(f"mkdir -p {fullpath}")

    def render_template_file(self, template_source, destination):
        template_path = os.path.join(self.templates_path, f"{template_source}.template")
        
        with open(template_path) as f:
            template_contents = f.read()

        template = Template(template_contents)
        with open(destination, 'w') as f:
            f.write(template.render(generator=self))            

    def create_structure_files(self):
        print(f">>> Creating file structure: {self.android_prefix}.{self.name}")

        main_files = self.main_project_files()
        for template_source in main_files:
            destination = f"{self.project_folder()}/{main_files[template_source]}"
            print(f"    Creating Android File: {destination}")
            self.render_template_file(template_source, destination)

        copy_files = self.main_copy_files()
        for source in copy_files:
            destination = f"{self.project_folder()}/{copy_files[source]}"
            print(f"    Copying Android File: {destination}")
            copyfile(f"takeoff/file_resources/android/{source}", destination)

    def main_project_folders(self):
        return [
            f"app/src/androidTest/java/{self.android_prefix.replace('.', '/')}",
            f"app/src/main/java/{self.android_prefix.replace('.', '/')}",
            f"app/src/main/java/{self.android_prefix.replace('.', '/')}/models",
            f"app/src/main/java/{self.android_prefix.replace('.', '/')}/services",
            f"app/src/main/java/{self.android_prefix.replace('.', '/')}/restclient",
            'app/src/main/res/drawable-v24',
            'app/src/main/res/drawable',
            'app/src/main/res/layout',
            'app/src/main/res/mipmap-anydpi-v26',
            'app/src/main/res/mipmap-hdpi',
            'app/src/main/res/mipmap-mdpi',
            'app/src/main/res/mipmap-xhdpi',
            'app/src/main/res/mipmap-xxhdpi',
            'app/src/main/res/mipmap-xxxhdpi',
            'app/src/main/res/values-night',
            'app/src/main/res/values',
            f"app/src/test/java/{self.android_prefix.replace('.', '/')}",
            'gradle/wrapper'
        ]
    
    def main_project_files(self):
        package_path = self.android_prefix.replace('.', '/')

        return {
            '.gitignore': '.gitignore',
            'app/build.gradle': 'app/build.gradle',
            'app/src/androidTest/java/ExampleInstrumentedTest.kt': f"app/src/androidTest/java/{package_path}/ExampleInstrumentedTest.kt",
            'app/src/test/java/ExampleUnitTest.kt': f"app/src/test/java/{package_path}/ExampleUnitTest.kt",            
            'app/src/main/AndroidManifest.xml': 'app/src/main/AndroidManifest.xml',
            'app/src/main/java/MainActivity.kt': f"app/src/main/java/{package_path}/MainActivity.kt",
            'app/src/main/res/values/themes.xml': 'app/src/main/res/values/themes.xml',
            'app/src/main/res/values/strings.xml': 'app/src/main/res/values/strings.xml',
            'app/src/main/res/values-night/themes.xml': 'app/src/main/res/values-night/themes.xml',
            'settings.gradle': 'settings.gradle',
            'local.properties': 'local.properties',
            'app/src/main/java/models/RestEntity.kt': f"app/src/main/java/{package_path}/models/RestEntity.kt",
            'app/src/main/java/restclient/ApiController.kt': f"app/src/main/java/{package_path}/restclient/ApiController.kt",
            'app/src/main/java/restclient/ProjectApiConnector.kt': f"app/src/main/java/{package_path}/restclient/{self.camelize(self.name)}ApiConnector.kt",
            'app/src/main/java/restclient/ServiceInterface.kt': f"app/src/main/java/{package_path}/restclient/ServiceInterface.kt",
            'app/src/main/java/restclient/VolleyMultipartRequest.kt': f"app/src/main/java/{package_path}/restclient/VolleyMultipartRequest.kt",
            'app/src/main/java/restclient/VolleyService.kt': f"app/src/main/java/{package_path}/restclient/VolleyService.kt",
            'app/src/main/java/services/RestEntityService.kt': f"app/src/main/java/{package_path}/services/RestEntityService.kt",
            'app/src/main/java/services/RestEntityServiceDelegate.kt': f"app/src/main/java/{package_path}/services/RestEntityServiceDelegate.kt",
        }
    
    def main_copy_files(self):
        return {
            'app/proguard-rules.pro': 'app/proguard-rules.pro',
            'app/src/main/res/drawable-v24/ic_launcher_foreground.xml': 'app/src/main/res/drawable-v24/ic_launcher_foreground.xml',
            'app/src/main/res/drawable/ic_launcher_background.xml': 'app/src/main/res/drawable/ic_launcher_background.xml',
            'app/src/main/res/layout/activity_main.xml': 'app/src/main/res/layout/activity_main.xml',
            'app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml': 'app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml',
            'app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml': 'app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml',
            'app/src/main/res/mipmap-hdpi/ic_launcher.png': 'app/src/main/res/mipmap-hdpi/ic_launcher.png',
            'app/src/main/res/mipmap-hdpi/ic_launcher_round.png': 'app/src/main/res/mipmap-hdpi/ic_launcher_round.png',
            'app/src/main/res/mipmap-mdpi/ic_launcher.png': 'app/src/main/res/mipmap-mdpi/ic_launcher.png',
            'app/src/main/res/mipmap-mdpi/ic_launcher_round.png': 'app/src/main/res/mipmap-mdpi/ic_launcher_round.png',
            'app/src/main/res/mipmap-xhdpi/ic_launcher.png': 'app/src/main/res/mipmap-xhdpi/ic_launcher.png',
            'app/src/main/res/mipmap-xhdpi/ic_launcher_round.png': 'app/src/main/res/mipmap-xhdpi/ic_launcher_round.png',
            'app/src/main/res/mipmap-xxhdpi/ic_launcher.png': 'app/src/main/res/mipmap-xxhdpi/ic_launcher.png',
            'app/src/main/res/mipmap-xxhdpi/ic_launcher_round.png': 'app/src/main/res/mipmap-xxhdpi/ic_launcher_round.png',
            'app/src/main/res/mipmap-xxxhdpi/ic_launcher.png': 'app/src/main/res/mipmap-xxxhdpi/ic_launcher.png',
            'app/src/main/res/mipmap-xxxhdpi/ic_launcher_round.png': 'app/src/main/res/mipmap-xxxhdpi/ic_launcher_round.png',
            'app/src/main/res/values/colors.xml': 'app/src/main/res/values/colors.xml',
            'build.gradle': 'build.gradle',
            'gradle.properties': 'gradle.properties',
            'gradle/wrapper/gradle-wrapper.jar': 'gradle/wrapper/gradle-wrapper.jar',
            'gradle/wrapper/gradle-wrapper.properties': 'gradle/wrapper/gradle-wrapper.properties',
            'gradlew': 'gradlew',
            'gradlew.bat': 'gradlew.bat',
        }