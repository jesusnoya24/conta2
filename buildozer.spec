[app]
title = Contador de Asistentes
package.name = contador
package.domain = org.contador
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_dirs = tests, bin, venv, .github, .git
version = 0.3
icon.filename = %(source.dir)s/icon.png
requirements = python3,kivy,pyjnius
p4a.branch = v2024.01.21
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a, armeabi-v7a
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
