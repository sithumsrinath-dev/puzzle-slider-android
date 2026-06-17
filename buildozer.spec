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
# Windows සතු kivy-deps ඉවත් කර Android සඳහා 100% ස්ථාවර පැකේජ පමණක් ඇතුළත් කර ඇත.
requirements = python3,kivy==2.3.0,openssl,requests,urllib3,certifi

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# =============================================================================
# Android specific configuration
# =============================================================================

# (list) Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (int) Target Android API (Play Store 2026 Requirement - API 34)
android.api = 34
android.target_api = 34

# (int) Minimum API your APK/AAB will support.
android.minapi = 21

# (bool) Use --private data storage (recommended)
android.private_storage = True

# (list) Architectures to build for (Play Store requires 64-bit arm64-v8a)
android.archs = arm64-v8a, armeabi-v7a

# (bool) Skip byte compile for .py files
android.skip_byte_compile = False

# =============================================================================
# Docker Engine Path Overrides
# =============================================================================
# Docker Container එක ඇතුළත පද්ධතිය විසින්ම ස්වයංක්‍රීයව කළමනාකරණය කරන නිවැරදි මාර්ගයන් යොදා ඇත.
android.sdk_path = 
android.ndk_path = 

# =============================================================================
# Buildozer configurations
# =============================================================================

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
# Root ප්‍රශ්න මඟහැරීමට මෙය අනිවාර්යයෙන්ම 0 විය යුතුය.
warn_on_root = 0
