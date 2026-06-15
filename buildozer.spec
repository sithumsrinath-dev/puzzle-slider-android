[app]
title = Ultimate Sliding Puzzle
package.name = puzzleslider
package.domain = org.silentthoughts
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# KivyMD සහ Pillow (Graphics) අවශ්‍යතා නිවැරදිව ඇතුළත් කර ඇත
requirements = python3,kivy==2.3.0,kivymd==1.1.1,pillow,openssl,requests,urllib3

# Icon settings
icon.filename = %(source.dir)s/icon.jpg

# Supported orientations
orientation = portrait

# Android Configurations
fullscreen = 1

# Play Store එකට දැමීමේදී arm64-v8a සහ armeabi-v7a යන දෙකම තිබීම අනිවාර්ය වේ
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# App එක Play Store එකට දාන්න .aab (Android App Bundle) එකක් ලෙස නිපදවීමට මෙය True කරන්න
android.release_artifact = aab

# Permissions (ජාල සම්බන්ධතාවය පරීක්ෂා කිරීමට අවශ්‍ය වේ)
android.permissions = INTERNET, ACCESS_NETWORK_STATE

[buildozer]
log_level = 2
warn_on_root = 0
