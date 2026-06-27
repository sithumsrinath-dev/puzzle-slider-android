[STRICT ENFORCEMENT - EXECUTIVE LEVEL DEVOPS COMMAND]

ඔබගේ GitHub Actions පරිසරය තුළ ඇප් එක බිල්ඩ් කිරීමේදී ඇති වන ගැටළු (Black Screen/Crash) මඟහරවා ගැනීම සඳහා, නිශ්චිතවම SDK 35 අනුකූලතාවය, නිවැරදි NDK/Architecture පරාමිතීන් සහ Kivy-Android ප්‍රශස්තකරණයන් සහිතව සැකසූ අවසාන `buildozer.spec` ගොනුව පහත දැක්වේ. මෙම සැකසුම මඟින් Android 16 සිට 15 දක්වා සියලුම API මට්ටම් සඳහා උපරිම ස්ථායීතාවයක් සහතික කරනු ඇත.

```ini
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
requirements = python3,kivy,openssl,requests,urllib3,certifi,idna,charset-normalizer

# (str) python-for-android branch to use
p4a.branch = master

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (bool) Android SDK license agreement
android.accept_sdk_license = True

# =============================================================================
# Android specific configuration
# =============================================================================

# (list) Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (int) Target Android API
android.api = 35
android.target_api = 35

# (int) Minimum API support
android.minapi = 24

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage
android.private_storage = True

# (list) Architectures to build for (Prevents Black Screen / Native library issues)
android.archs = arm64-v8a, armeabi-v7a

# (str) The format used to package the app
android.release_artifact = aab

# (bool) Skip byte compile for .py files
android.skip_byte_compile = False

# (str) Presplash color background
android.presplash_color = #000000

# (list) Android meta-data
android.meta_data = android.app.lib_name=main

# =============================================================================
# Buildozer configurations
# =============================================================================

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 0

# (str) Path to build artifact storage
build_dir = .buildozer

```
