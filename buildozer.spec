# buildozer.spec

[app]

# (string) Title of your application
title = Ultimate Sliding Puzzle

# (string) Package name
package.name = slidingpuzzle

# (string) Package domain (needed for android packaging)
package.domain = com.senu.puzzle

# (string) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (str) Presplash of the application
presplash.filename = %(source.dir)s/presplash.jpg

# (str) Application version
version = 1.0.1

# (list) Application requirements
requirements = python3,kivy,html5lib,openssl,requests,urllib3,certifi

# (str) python-for-android branch to use, defaults to master
p4a.branch = master

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# Android SDK ලිපිදේය එකඟතාවය
android.accept_sdk_license = True

# =============================================================================
# Android specific configuration
# =============================================================================

# (list) Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (int) Target Android API, optimized for Android 16 and backward compatibility
android.api = 35
android.target_api = 35

# (int) Minimum API your APK/AAB will support.
android.minapi = 24

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (recommended)
android.private_storage = True

# (list) Architectures to build for (Prevents Black Screen on modern devices)
android.archs = arm64-v8a, armeabi-v7a

# (str) The format used to package the app
android.release_artifact = aab

# (bool) Skip byte compile for .py files
android.skip_byte_compile = False

# =============================================================================
# Buildozer configurations
# =============================================================================

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0
