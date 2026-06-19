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
version = 1.0.1  # පියවර 3 අනුව 1.0.0 වෙනුවට 1.0.1 ලෙස වෙනස් කරන්න.

# (list) Application requirements
# නව Cython 3 සමඟ ඇතිවන ගැටුම් වැළැක්වීමට cython==0.29.33 ලෙස එක් කර ඇත.
requirements = python3,kivy==2.3.0,cython==0.29.33,openssl,requests,urllib3,certifi

# (str) python-for-android branch to use, defaults to master
# පද්ධතිය Python 3.14 වෙත යාවත්කාලීන වීම නැවැත්වීම සඳහා අතිශය ස්ථායී v2024.01.21 සංස්කරණයට අගුලු දමා ඇත.
p4a.branch = v2024.01.21

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# =============================================================================
# Android specific configuration
# =============================================================================

# (list) Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (int) Target Android API (API 34 - Google Play 2024/2025/2026 Standards)
android.api = 34
android.target_api = 34

# (int) Minimum API your APK/AAB will support
android.minapi = 24

# (str) Android NDK version to use (Force Stable Version to prevent Compiler Crash)
android.ndk = 25b

# (bool) Use --private data storage (recommended)
android.private_storage = True

# (list) Architectures to build for (Strictly 64-bit for modern Android/Play Store)
android.archs = arm64-v8a

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
