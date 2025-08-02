[app]
title = aiDroid
package.name = aidroid
package.domain = org.daydaylx
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,json,ttf
version = 1.0.0
requirements = python3,kivy,kivymd,httpx
orientation = portrait
fullscreen = 1
android.permissions = INTERNET

# (optional) API-Key über Umgebungsvariable setzen
android.exported = True
android.allow_backup = True

# Icons und Assets (optional)
icon.filename = %(source.dir)s/assets/icon.png

# Buildozer intern
log_level = 2
warn_on_root = 1

[buildozer]
log_level = 2
warn_on_root = 1

# Android-Spezifikationen
android.api = 33
android.minapi = 28
android.ndk = 25b
android.sdk = 24
android.ndk_path = 
android.sdk_path = 
android.arch = arm64-v8a
android.private_storage = True

# Damit Kivy mit Async/Await und httpx funktioniert
android.enable_androidx = True
android.gradle_dependencies = androidx.appcompat:appcompat:1.4.2
