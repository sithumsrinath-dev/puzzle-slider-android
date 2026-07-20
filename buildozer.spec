[app]
title = Puzzle Slider
package.name = puzzleslider
package.domain = org.sithumsrinath
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
source.include_patterns = assets/*,images/*.png
version = 1.0.0
requirements = python3,kivy,six,filetype,urllib3,certifi,chardet,requests,idna,openssl
android.archs = armeabi-v7a, arm64-v8a
icon.filename = icon.png
presplash.filename = presplash.jpg
orientation = portrait
fullscreen = 1
android.permissions = INTERNET
android.api = 34
android.minapi = 24
android.ndk = 25b
android.private_storage = True
android.copy_libs = 1
android.accept_sdk_license = True
android.release_artifact = aab
log_level = 2
warn_on_root = 1

[buildozer]
log_level = 2
warn_on_root = 1
