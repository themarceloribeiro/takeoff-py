import os
from jinja2 import Template
from .android_base_generator import AndroidBaseGenerator
from pathlib import Path
from shutil import copyfile

class AndroidAuthenticationGenerator(AndroidBaseGenerator):

    def run(self):
        self.facebook_auth = False
        self.facebook_app_id = None
        self.facebook_scheme = None

        self.setup()
        print(f">>> Running Android Authentication Generator: {self.name}")
        self.create_structure_folders()
        self.create_structure_files()
        self.add_user_attributes()
        self.add_manifest_activity(f"        <activity android:name=\".user_auth.LoginSignupActivity\"/>")
        self.add_main_activity_methods()
        self.add_application_launched_callback()
        self.add_login_strings()

        for option in self.options:
            if 'facebook_auth' in option and option.split('=')[1].lower() == 'true':
                self.facebook_auth = True
            if 'facebook_app_id' in option:
                self.facebook_app_id = option.split('=')[1]
            if 'facebook_scheme' in option:
                self.facebook_scheme = option.split('=')[1]

        if self.facebook_auth and self.validate_facebook_settings():
            self.add_facebook_auth()

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
        self.add_import_line(destination, f"{self.android_prefix}.user_auth.LoginSignupActivity")

        userLoggedIn = ("\n").join([
            "    fun userLoggedIn(): Boolean {",
            "       val user = currentUser()",
            "       return user != null && user.token != null",
            "    }"
        ])

        presentLogin = ("\n").join([
            "    fun presentLogin() {",
            "       startActivity(Intent(this, LoginSignupActivity::class.java))",
            "    }"
        ])

        self.add_method_to_class('main/MainActivity.kt', userLoggedIn, 'userLoggedIn')
        self.add_method_to_class('main/MainActivity.kt', presentLogin, 'presentLogin')

    def add_application_launched_callback(self):
        lines = ("\n").join([
            "        // UserAuth Check - do not remove",
            "        if(userLoggedIn()) {",
            "           presentHome()",
            "        } else {\n",
            "           presentLogin()",
            "        }"
        ])

        self.replace_lines_for_method('main/MainActivity.kt', 'fun applicationDidLaunch', lines)


    def validate_facebook_settings(self):
        return self.facebook_app_id != None and self.facebook_scheme != None

    def add_facebook_auth(self):
        self.add_string_value('facebook_app_id', self.facebook_app_id)
        self.add_string_value('fb_login_protocol_scheme', self.facebook_scheme)
        self.add_manifest_activity(
            ("\n".join([
                '        <activity android:name="com.facebook.FacebookActivity"',
                '           android:configChanges="keyboard|keyboardHidden|screenLayout|screenSize|orientation"',
                '           android:label="@string/app_name" />'
            ]))
        )
        self.add_manifest_activity(
            ("\n").join([
                '        <activity android:name="com.facebook.CustomTabActivity" android:exported="true">',
                '            <intent-filter>',
                '                <action android:name="android.intent.action.VIEW" />',
                '                <category android:name="android.intent.category.DEFAULT" />',
                '                <category android:name="android.intent.category.BROWSABLE" />',
                '                <data android:scheme="@string/fb_login_protocol_scheme" />',
                '            </intent-filter>',
                '        </activity>'
            ])
        )

        self.add_manifest_metadata(
            ("\n").join([
                '        <meta-data android:name="com.facebook.sdk.ApplicationId"',
                '           android:value="@string/facebook_app_id"/>'
            ])
        )

        self.add_gradle_implementation('com.facebook.android:facebook-login:8.1.0')

        self.add_layout_component(
            'login_signup_activity.xml',
            ("\n").join([
                '    <com.facebook.login.widget.LoginButton',
                '        android:id="@+id/facebookLoginButton"',
                '        android:layout_width="wrap_content"',
                '        android:layout_height="50dp"',
                '        android:layout_marginBottom="200dp"',
                '        app:layout_constraintBottom_toBottomOf="parent"',
                '        android:layout_marginLeft="0dp"',
                '        app:layout_constraintLeft_toLeftOf="parent"',
                '        android:layout_marginRight="0dp"',
                '        app:layout_constraintRight_toRightOf="parent"',
                '        />',
            ])
        )

        destination = f"{self.project_folder()}/app/src/main/java/{self.android_prefix.replace('.', '/')}/user_auth/LoginSignupActivity.kt"
        self.add_import_line(destination, 'android.util.Log')
        self.add_import_line(destination, 'java.util.*')
        self.add_import_line(destination, 'com.facebook.CallbackManager')
        self.add_import_line(destination, 'com.facebook.FacebookCallback')
        self.add_import_line(destination, 'com.facebook.FacebookException')
        self.add_import_line(destination, 'com.facebook.GraphRequest')
        self.add_import_line(destination, 'com.facebook.login.LoginManager')
        self.add_import_line(destination, 'com.facebook.login.LoginResult')
        self.add_import_line(destination, f"{self.android_prefix}.services.LoginService")
        self.add_line_before_pattern(destination, "\n", 'class ', True)

        self.add_attribute_to_activity("user_auth/LoginSignupActivity.kt", "callbackManager", "CallbackManager.Factory.create()")
        self.add_attribute_to_activity("user_auth/LoginSignupActivity.kt", "SCOPE", "\"email, public_profile\"")
        self.add_line_before_pattern(destination, "\n", 'override fun onCreate', True)

        registerFacebookListeners = ("\n").join([
            '    fun registerFacebookListeners() {',
            '        LoginManager.getInstance().registerCallback(callbackManager,',
            '            object : FacebookCallback<LoginResult?> {',
            '                override fun onSuccess(loginResult: LoginResult?) {',
            '                    facebookLoggedIn(loginResult)',
            '                }',
            '',
            '                override fun onCancel() {',
            '                    facebookCanceled()',
            '                }',
            '',
            '                override fun onError(exception: FacebookException) {',
            '                    facebookError(exception)',
            '                }',
            '            })',
            '    }',
        ])

        self.add_method_to_class('user_auth/LoginSignupActivity.kt', registerFacebookListeners, 'registerFacebookListeners')

        facebookError = ("\n").join([
            '    private fun facebookError(exception: FacebookException) {',
            '        displayError("Error with facebook login: ${exception.toString()}")',
            '    }',
        ])

        self.add_method_to_class('user_auth/LoginSignupActivity.kt', facebookError, 'facebookError')

        facebookCanceled = ("\n").join([
            '    private fun facebookCanceled() {',
            '        displayError("User canceled facebook login")',
            '    }',
        ])

        self.add_method_to_class('user_auth/LoginSignupActivity.kt', facebookCanceled, 'facebookCanceled')

        facebookLoggedIn = ("\n").join([
            '    private fun facebookLoggedIn(loginResult: LoginResult?) {',
            '        val request = GraphRequest.newMeRequest(',
            '            loginResult!!.accessToken',
            '        ) { jsonObject, response ->',
            '            var m = LoginService',
            '            m.delegate = this',
            '            m.login(',
            '                jsonObject.get("email").toString(),',
            '                "",',
            '                jsonObject.get("name").toString().split(" ").first(),',
            '                jsonObject.get("name").toString().split(" ").last(),',
            '                "facebook",',
            '                jsonObject.get("id").toString()',
            '            )',
            '        }',
            '',
            '        val parameters = Bundle()',
            '        parameters.putString("fields", "id,name,link,email")',
            '        request.parameters = parameters',
            '        request.executeAsync()',
            '     }',
        ])

        self.add_method_to_class('user_auth/LoginSignupActivity.kt', facebookLoggedIn, 'facebookLoggedIn')

        onActivityResult = ("\n").join([
            '    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {',
            '        callbackManager.onActivityResult(requestCode, resultCode, data)',
            '        super.onActivityResult(requestCode, resultCode, data)',
            '    }',
        ])

        self.add_method_to_class('user_auth/LoginSignupActivity.kt', onActivityResult, 'onActivityResult')

        lines = ("\n").join([
            '        // FacebookAuthCheck - do not remove',
            '        facebookLoginButton.setReadPermissions(Arrays.asList(SCOPE))',
            '        registerFacebookListeners()',
        ])

        self.append_lines_to_method('user_auth/LoginSignupActivity.kt', 'fun onCreate', lines)

        print("Facebook Auth OK")

    def add_user_attributes(self):
        self.add_attribute_to_entity('User', 'first_name', 'String')
        self.add_attribute_to_entity('User', 'last_name', 'String')
        self.add_attribute_to_entity('User', 'email', 'String')
        self.add_attribute_to_entity('User', 'password', 'String', True)
        self.add_attribute_to_entity('User', 'token', 'String', False, True, True)

    def add_login_strings(self):
        self.add_string_value('login', 'Login')
        self.add_string_value('have_an_account', 'Have an account?')
        self.add_string_value('log_in', 'Log in')
        self.add_string_value('dont_have_account', "Don\\'t have an account")
        self.add_string_value('sign_up', 'Sign up')
        self.add_string_value('forgot', 'Forgot your password?')
        self.add_string_value('password', 'Password?')
        self.add_string_value('login_hint', 'E-mail')
