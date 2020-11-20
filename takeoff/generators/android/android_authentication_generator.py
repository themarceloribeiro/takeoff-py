import os
from jinja2 import Template
from .android_base_generator import AndroidBaseGenerator
from pathlib import Path
from shutil import copyfile

class AndroidAuthenticationGenerator(AndroidBaseGenerator):

    def run(self):
        self.setup()
        print(f">>> Running Android Authentication Generator: {self.name}")
        self.create_structure_folders()
        self.create_structure_files()
        self.add_user_attributes()
        self.add_manifest_activity('.user_auth.LoginSignupActivity')
        self.add_main_activity_methods()
        self.add_application_launched_callback()

    def create_structure_folders(self):
        print(f">>> Creating directory structure: {self.android_prefix}.{self.name}")

        for folder in self.main_project_folders():
            fullpath = f"{self.project_folder()}/{folder}"
            print(f"    Creating Android Folder: {fullpath}")
            os.system(f"mkdir -p {fullpath}")

    def create_structure_files(self):
        print(f">>> Creating file structure: {self.android_prefix}.{self.name}")

        main_files = self.main_project_files()
        for template_source in main_files:
            destination = f"{self.project_folder()}/{main_files[template_source]}"
            print(f"    Creating Android File: {destination}")
            self.render_template(f"{self.templates_path}/{template_source}.template", destination, False)

        copy_files = self.main_copy_files()
        for source in copy_files:
            destination = f"{self.project_folder()}/{copy_files[source]}"
            print(f"    Copying Android File: {destination}")
            copyfile(f"takeoff/file_resources/android/{source}", destination)

    def main_project_folders(self):
        return [
            f"app/src/main/java/{self.android_prefix.replace('.', '/')}/user_auth",
        ]
    
    def main_project_files(self):
        package_path = self.android_prefix.replace('.', '/')

        return {
            'app/src/main/java/services/LoginService.kt': f"app/src/main/java/{package_path}/services/LoginService.kt",
            'app/src/main/java/services/LoginServiceDelegate.kt': f"app/src/main/java/{package_path}/services/LoginServiceDelegate.kt",
            'app/src/main/java/services/UserService.kt': f"app/src/main/java/{package_path}/services/UserService.kt",
            'app/src/main/java/user_auth/LoginFragment.kt': f"app/src/main/java/{package_path}/user_auth/LoginFragment.kt",
            'app/src/main/java/user_auth/SignupFragment.kt': f"app/src/main/java/{package_path}/user_auth/SignupFragment.kt",
            'app/src/main/java/user_auth/LoginSignupActivity.kt': f"app/src/main/java/{package_path}/user_auth/LoginSignupActivity.kt",
            'app/src/main/res/layout/login_fragment.xml': f"app/src/main/res/layout/login_fragment.xml",
            'app/src/main/res/layout/signup_fragment.xml': f"app/src/main/res/layout/signup_fragment.xml",
            'app/src/main/res/layout/login_signup_activity.xml': f"app/src/main/res/layout/login_signup_activity.xml",
        }
    
    def main_copy_files(self):
        return {
            'app/proguard-rules.pro': 'app/proguard-rules.pro',
        }
    
    def add_main_activity_methods(self):
        destination = f"{self.project_folder()}/app/src/main/java/{self.android_prefix.replace('.', '/')}/main/MainActivity.kt"
        new_line = f"import {self.android_prefix}.user_auth.LoginSignupActivity"

        self.add_line_before_pattern(destination, new_line, 'class ')

        userLoggedIn = ("\n").join([
            "fun userLoggedIn(): Boolean {",
            "   val user = currentUser()",
            "   return user != null && user.token != null",
            "}"
        ])

        presentLogin = ("\n").join([
            "fun presentLogin() {",
            "   startActivity(Intent(this, LoginSignupActivity::class.java))",
            "}"
        ])

        self.add_method_to_class('main/MainActivity.kt', userLoggedIn, 'userLoggedIn')
        self.add_method_to_class('main/MainActivity.kt', presentLogin, 'presentLogin')
    
    def add_application_launched_callback(self):
        lines = [
            "if(userLoggedIn()) {\n",
            "   presentHome()\n",
            "} else {\n",
            "   presentLogin()\n",
            "}\n"
        ]

        self.replace_lines_for_method('main/MainActivity.kt', 'applicationDidLaunch', lines)
    
    def add_user_attributes(self):
        self.add_attribute_to_entity('User', 'first_name', 'string')
        self.add_attribute_to_entity('User', 'last_name', 'string')
        self.add_attribute_to_entity('User', 'email', 'string')
        self.add_attribute_to_entity('User', 'password', 'String')
        self.add_attribute_to_entity('User', 'password_confirmation', 'String')
        self.add_attribute_to_entity('User', 'token', 'String')