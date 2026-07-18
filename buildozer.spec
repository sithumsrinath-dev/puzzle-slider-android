[app]

# (str) Title of your application
title = Puzzle Slider

# (str) Package name
package.name = puzzleslider

# (str) Package domain (needed for android packaging)
package.domain = org.senu

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to exclude nothing)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to exclude nothing)
#source.exclude_dirs = tests, bin, venv

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/ignored.*

# (str) Application version method (see requirements)
version = 1.0.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3==3.11.15,hostpython3==3.11.15,kivy==2.3.0,six,filetype,urllib3,certifi,chardet,requests,idna

# (str) Custom source folders for requirements
# These paths should be qualified, absolute-paths or relative to the spec file
# requirements.source.kivy = ../../kivy

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
presplash.filename = %(source.dir)s/presplash.jpg

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientations (valid options are: landscape, portrait, all)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT_TO_PY

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (string) Presplash background color (options: #RRGGBB, #AARRGGBB, 'none' or a web color name)
#android.presplash_color = #FFFFFF

# (string) Presplash animation duration in milliseconds (default is 0)
#android.presplash_lottie_duration = 0

# (list) Permissions
#android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 34

# (int) Minimum API your APK will support.
android.minapi = 24

# (int) Android SDK version to use
#android.sdk = 34

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
android.ndk_api = 24

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (page) Android entry point, default is to use start.py
#android.entrypoint = default.py

# (str) Android app theme, default is ok for kivi applications.
# android.apptheme = "@android:style/Theme.NoTitleBar.Fullscreen"

# (list) Pattern to whitelist for the whole project
#android.whitelist =

# (str) Path to a custom whitelist file
#android.whitelist_src =

# (str) Path to a custom blacklist file
#android.blacklist_src =

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jar that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching, for example:
# %(source.dir)s/libs/*.jar
#android.add_jars = foo.jar,bar.jar,path/to/a/*.jar

# (list) List of Java files to add to the android project (for custom java code)
#android.add_src =

# (list) Android AAR archives to add
#android.add_aars =

# (list) Java classes to keep as entrypoint (skip optimization given by proguard)
#android.add_activities = com.facebook.LoginActivity

# (list) Android manifests to add
#android.manifest.xml =

# (str) Android manifest intent filters to add
#android.manifest.intent_filters =

# (list) Android launch modes to set for main activity
#android.manifest.launch_mode = standard

# (list) Android additional libraries to copy into libs/armeabi
#android.add_libs_armeabi = libs/android-v7/libsqlite3_android.so
#android.add_libs_armeabi_v7a = libs/android-v7/libsqlite3_android.so
#android.add_libs_arm64_v8a = libs/android-v8/libsqlite3_android.so
#android.add_libs_x86 = libs/android-x86/libsqlite3_android.so
#android.add_libs_x86_64 = libs/android-x86_64/libsqlite3_android.so

# (list) Android architectures to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = armeabi-v7a, arm64-v8a

# (bool) Enable Android extra justification inside text layout
#android.manifest.justify = True

# (list) Android application arguments. You can reference package fields with { packages }
#android.args =

# (bool) Enable Gradle daemon (default is True)
#android.enable_gradle_daemon = True

# (str) target outputs given by the build. For Play Store release, use aab
android.release_artifact = aab

# (str) Log level (0 = error only, 1 = info, 2 = debug and big logs)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0

# (str) Path to build output directory (default is %(source.dir)s/bin)
#bin_dir = ./bin

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug and big logs)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0
