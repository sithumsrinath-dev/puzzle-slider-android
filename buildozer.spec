[app]
title = Ultimate Sliding Puzzle
package.name = puzzleslider
package.domain = org.silentthoughts
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy

# (X) Icon settings
icon.filename = %(source.dir)s/icon.jpg

# (X) Supported orientations
orientation = portrait

# (X) Android specific
osx.kivy_version = 2.3.0
fullscreen = 1
android.archs = arm64-v8a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 0
