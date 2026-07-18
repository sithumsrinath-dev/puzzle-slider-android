[app]

# (str) Title of your application
title = Puzzle Slider

# (str) Package name
package.name = puzzleslider

# (str) Package domain (needed for android packaging)
package.domain = org.sithumsrinath

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,images/*.png

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,six,filetype,urllib3,certifi,chardet,requests,idna

# (str) Custom source folders for requirements
# Custom architectures required
android.archs = armeabi-v7a, arm64-v8a

# (str) Icon of the application
icon.filename = icon.png

# (str) Presplash of the application
presplash.filename = presplash.jpg

# (str) Supported orientations (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 34

# (int) Minimum API your APK/AAB will support.
android.minapi = 24

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data directory (True) or --dir public storage (False)
android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded)
android.ndk_path = 

# (str) Android SDK directory (if empty, it will be automatically downloaded)
android.sdk_path = 

# (str) ANT directory (if empty, it will be automatically downloaded)
android.ant_path = 

# (bool) If True, then skip google play licensingapplications
android.skip_update = False

# (bool) Copy library instead of making a lib dir. Standard is False
android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# (list) Android application formats to build for (e.g. aab, apk)
android.formats = aab

# (bool) Accept SDK license without identifying input
android.accept_sdk_license = True

# (str) Log level (0 = error only, 1 = info, 2 = debug (full output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (full output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
