[app]
# (string) Title of your application
title = Ultimate Sliding Puzzle

# (string) Package name
package.name = slidingpuzzle

# (string) Package domain (needed for android packaging)
package.domain = com.senu.puzzle

# (string) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (string) Application version
version = 1.0.0

# (list) Application requirements
# Added openssl, requests, urllib3, and certifi for 100% secure stable UrlRequest
requirements = python3,kivy==2.3.0,kivy-deps.angle,kivy-deps.glew,kivy-deps.sdl2,openssl,requests,urllib3,certifi

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# =============================================================================
# Android specific configuration
# =============================================================================

# (list) Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible. (Play Store 2026 Target)
android.api = 34
android.target_api = 34

# (int) Minimum API your APK/AAB will support.
android.minapi = 21

# (str) Android NDK version to use (Stable for Kivy 2.3.0 + SDK 34)
android.ndk = 26b
android.ndk_api = 21

# (bool) Use --private data storage (recommended)
android.private_storage = True

# (list) list of Java .jar files to add to the libs so that pyobjus can use
# android.add_jars = foo.jar

# (list) Architectures to build for (Play Store requires 64-bit arm64-v8a)
android.archs = arm64-v8a, armeabi-v7a

# (bool) Skip byte compile for .py files
android.skip_byte_compile = False

# (str) The Android card id to features, for Google Play Billing metadata
# android.features = 

# =============================================================================
# Buildozer configurations
# =============================================================================

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
