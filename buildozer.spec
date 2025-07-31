[app]
title = aiDroid S25 Pro
package.name = aidroid
package.domain = org.daydaylx

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,xml
version = 2.0.0

# ULTRA-STABILE Requirements - garantiert verfügbare Versionen
requirements = python3,kivy,kivymd

icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

orientation = portrait
fullscreen = 0
android.presplash_color = #1565C0

# Minimal permissions für stabilen Build
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# Bewährte Android-Einstellungen
android.api = 30
android.minapi = 21
android.ndk = 23c
android.ndk_api = 21
android.private_storage = True
android.archs = arm64-v8a

p4a.bootstrap = sdl2
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
