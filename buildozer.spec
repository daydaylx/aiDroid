[app]
# ---------------------------
# Grundlegende App-Infos
# ---------------------------
title = aiDroid
package.name = aidroid
package.domain = org.daydaylx

# Quellcode & Assets
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,json,xml,atlas,ttf,otf,mp3,mp4,ogg,wav

version = 1.0.0

# ---------------------------
# Python & Abhängigkeiten
# ---------------------------
# Python 3.9 ist stabil kompatibel mit python-for-android (P4A)
requirements = python3==3.9,kivy==2.3.0,kivymd,requests,sqlite3,android,pyjnius,filetype,cython==0.29.33

# ---------------------------
# Geräteorientierung & Display
# ---------------------------
orientation = portrait
fullscreen = 0
android.presplash_color = #FFFFFF

# Icons
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

# ---------------------------
# Android Permissions (maximal sauber & Play Store kompatibel)
# Seit Android 13-15 muss man Media-Zugriffe separat angeben!
android.permissions = INTERNET,ACCESS_NETWORK_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,ACCESS_WIFI_STATE,MANAGE_EXTERNAL_STORAGE,READ_MEDIA_IMAGES,READ_MEDIA_VIDEO,READ_MEDIA_AUDIO,FOREGROUND_SERVICE

# ---------------------------
# Android Build Settings
# ---------------------------
# Setze API-Level passend zu S25 Android 15
android.api = 34
android.minapi = 26
android.sdk = 34

# Empfohlene stabile NDK Version für P4A
android.ndk = 25b
android.ndk_api = 26

# Private Lagerung der App-Daten für DSGVO & Store Compliance
android.private_storage = True

# Architektur für Snapdragon8 Gen4 / S25 (64-bit ARM)
android.archs = arm64-v8a

# Packaging Option für libc++
android.add_packaging_options = packagingOptions { pickFirst '**/libc++_shared.so' }

# ---------------------------
# python-for-android Settings
# ---------------------------
# Stable master branch
p4a.branch = master

# SDL2 bootstrap ist Standard für Kivy
p4a.bootstrap = sdl2

# ---------------------------
# Kivy Garden Widgets (eintragen falls benötigt)
# ---------------------------
garden_requirements =

# ---------------------------
# Buildozer Settings
# ---------------------------
[buildozer]
log_level = 2         # Für detaillierte Logs beim Build
warn_on_root = 1      # Warnung bei Ausführung als root (besser non-root!)

# Falls du eigene Gradle-Repos oder Dependencies brauchst
android.gradle_dependencies =
android.add_gradle_repositories =

