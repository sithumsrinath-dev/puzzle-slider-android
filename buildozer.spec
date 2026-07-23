[app]

# (str) Source code where the main.py live
source.dir = .

# (str) Title of your application
title = Puzzle Slider

# (str) Package name
package.name = puzzleslider

# (str) Package domain (needed for android packaging)
package.domain = org.senu

# (list) Source files to include (let git decide)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/,images/*.png

# (list) Source files to exclude (let git decide)
#source.exclude_exts = spec

# (list) List of directory to exclude
#source.exclude_dirs = tests, bin

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*.jpg

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,kivmob,pyobjus,android

# (list) Custom source folders for python modules
anzu = source.include_exts path
#source.dirs =

# (str) Presplash of the application
presplash.filename = %(source.dir)s/presplash.jpg

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (list) Supported orientations
# Valid orientations: landscape, portrait, all-upright, all-reverse or reverse-landscape; or a comma-separated list of these
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PYTHON_SCRIPT,...,NAME:ENTRYPOINT_TO_PYTHON_SCRIPT

# OSX Specific
# Author
# (int) Target Android API, should be as high as possible.  
android.api = 34  

# (int) Minimum API your APK will support.  
android.minapi = 21  

# (int) Android SDK version to use  
android.sdk = 34  

# (str) Android NDK version to use  
android.ndk = 25b  

# (int) Android NDK API to use. This is the minimum API supported by your app.
#android.ndk_api = 21

# (bool) Use --private data storage (True) or --public storage (False)
#android.private_storage = True

# (list) Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (list) features (adds tags to AndroidManifest.xml)
#android.features = android.hardware.usb.host

# (str) Bootstrap to use for android builds
#android.bootstrap = sdl2

# (str) XML file to inject into AndroidManifest.xml
#android.manifest.xml =

# (str) Extra XML files to inject into AndroidManifest.xml
android.manifest.application_inject =

# (str) Extra Java classes to add
#android.add_java_jar =

# (str) Extra Java sources to add
#android.add_java_src =

# (str) Gradle dependencies to add
android.add_gradle_dependencies = com.google.android.gms:play-services-ads:22.6.0

# (list) Application meta-data to add (key=value)
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-5106431642894326~3643301881

# (bool) Enable AndroidX support
android.androidx = True

# (list) AAR libraries to load
#android.aar_libs =

# (list) The comma-separated list of extra directories to add to the python path
#android.add_python_path =

# (list) List of Java .jar files to add to the libs/ directory
#android.add_jars =

# (list) The comma-separated list of additional assets to pack in the APK
#android.add_assets =

# (list) Gradle repositories to add
#android.gradle_repositories =

# (bool) Copy library to the build dir when using --private-storage=True
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) Enables Android Lint inspection
#android.lint = False

# (bool) Enable use of incremental builds
#android.incremental = False

# (str) python-for-android branch to use
#p4a.branch = master

# (str) Ouput format, either apk or aar or aab
android.output_format = aab

[buildozer]

# (int) Log level (0 = error, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_root = 1

# (str) Path to build artifact, default is ./.buildozer
#bin_dir = ./bin

# (str) Path to extra buildozer dir
#build_dir = ~/.buildozer

# (str) Builder cache directory
#cache_dir = ~/.buildozer/cache

# (str) Android platform API version
#android.platform_api = 34

# (str) Accept SDK license
android.accept_sdk_license = True
