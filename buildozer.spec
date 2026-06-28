[app]
title = Ultimate Sliding Puzzle
package.name = slidingpuzzle
package.domain = com.senu.puzzle
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.jpg
version = 1.0.1
requirements = python3,kivy,openssl,requests,urllib3,certifi,idna,charset-normalizer
p4a.branch = master
orientation = portrait
fullscreen = 1
android.accept_sdk_license = True
android.permissions = INTERNET, ACCESS_NETWORK_STATE
android.api = 35
android.target_api = 35
android.minapi = 24
android.ndk = 25b
android.private_storage = True
android.archs = arm64-v8a, armeabi-v7a
android.release_artifact = aab
android.skip_byte_compile = False
android.meta_data = android.app.lib_name=main
android.presplash_color = #000000
android.entrypoint = org.kivy.android.PythonActivity
android.opengl_backend = gl

[buildozer]
log_level = 2
warn_on_root = 0
build_dir = .buildozer
