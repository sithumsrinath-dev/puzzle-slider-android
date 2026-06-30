[app]
title = Sliding Puzzle
package.name = slidingpuzzle
package.domain = org.senu.games

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,wav,ogg

version = 1.0.0

requirements = python3==3.11.9,kivy==2.3.0

icon.filename = icon.png
presplash.filename = presplash.jpg

orientation = portrait
fullscreen = 0

android.permissions = INTERNET, WAKE_LOCK

android.api = 34
android.minapi = 24
android.ndk = 25b
android.ndk_api = 24
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
