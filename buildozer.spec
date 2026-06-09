[app]
title = Ultimate Sliding Puzzle
package.name = puzzleslider
package.domain = org.silentthoughts
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# GitHub Actions සඳහා වඩාත් ගැලපෙනම දේවල් එකතු කර ඇත
requirements = python3,kivy==2.3.0,openssl,requests,urllib3

# Icon settings
icon.filename = %(source.dir)s/icon.jpg

# Supported orientations
orientation = portrait

# Android Configurations (සිස්ටම් එකටම කැමති NDK එකක් ගන්න ඉඩ දී ඇත)
fullscreen = 1
android.archs = arm64-v8a
android.allow_backup = True

# Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE

[buildozer]
log_level = 2
warn_on_root = 0
