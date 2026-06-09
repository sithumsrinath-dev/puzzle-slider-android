[app]
title = Ultimate Sliding Puzzle
package.name = puzzleslider
package.domain = org.silentthoughts
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# ඉන්ටර්නෙට් සහ ආරක්ෂිත දත්ත සඳහා අවශ්‍ය දේවල් එකතු කර ඇත
requirements = python3,kivy==2.3.1,openssl,requests,urllib3

# Icon settings
icon.filename = %(source.dir)s/icon.jpg

# Supported orientations
orientation = portrait

# Android specific configurations
fullscreen = 1
android.archs = arm64-v8a
android.allow_backup = True

# ඇප් එක ඇතුළෙන් ඉන්ටර්නෙට් පාවිච්චි කරන්න අවසර දීම (Ad verification සඳහා)
android.permissions = INTERNET, ACCESS_NETWORK_STATE

[buildozer]
log_level = 2
warn_on_root = 0
