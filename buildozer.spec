[app]
title = Ultimate Sliding Puzzle
package.name = puzzleslider
package.domain = org.silentthoughts
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# වඩාත් ස්ථාවර Kivy සහ අවශ්‍ය Dependencies
requirements = python3,kivy==2.3.0,openssl,requests,urllib3

# Icon settings
icon.filename = %(source.dir)s/icon.jpg

# Supported orientations
orientation = portrait

# Android configurations (ස්ථාවර සංස්කරණ බලෙන්ම නියම කර ඇත)
fullscreen = 1
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a
android.allow_backup = True

# Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE

[buildozer]
log_level = 2
warn_on_root = 0
