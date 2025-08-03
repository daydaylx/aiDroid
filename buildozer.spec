[app]

# Name deiner App (Pflicht)
title = aiDroid S25 Pro

# Interner Paketname (Pflicht, nur Kleinbuchstaben, keine Leerzeichen)
package.name = aindroids25pro

# Domain (Pflicht, eindeutig)
package.domain = org.daydaylx

# Hauptquellcode-Verzeichnis (meist ".")
source.dir = .

# App-Version (Pflicht)
version = 1.0.0

# Icon & Presplash (Dateien müssen existieren)
icon.filename = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/presplash.png

# Anforderungen (je nach App!)
requirements = python3,kivy,requests,sqlite3

# Zusätzliche zu includende Dateien/Ordner (Optional)
# source.include_exts = py,png,jpg,kv,atlas,json,ttf,otf,xml,md
# source.include_dirs = assets,libs

# Android Berechtigungen (nur was du wirklich brauchst)
permissions = android.permission.INTERNET,android.permission.ACCESS_NETWORK_STATE

# NDK, SDK, API usw. (empfohlen: nicht ändern wenn alles läuft)
android.ndk_version = 25b
android.sdk_version = 33
android.build_tools_version = 33.0.0
android.api = 33

# Automatisch SDK-Lizenzen akzeptieren (Pflicht für CI)
android.accept_sdk_license = True

# ProGuard: Ja, wenn du Java/Obfuscation brauchst, sonst False
android.use_proguard = False
# android.proguard_rules = proguard-rules.pro

# (Optional) Orientation fixieren
# orientation = portrait

# (Optional) Activities, Services, Permissions (wenn gebraucht)
# android.add_a_permissions = android.permission.CAMERA
# android.add_a_activities = org.kivy.MyCustomActivity
# android.add_a_services = org.kivy.MyService

# (Optional) Minimum unterstützte API (wenn du alte Geräte brauchst)
# android.minapi = 21

# (Optional) Android App Bundle (AAB statt APK)
# android.aab = False

# (Optional) Entry Point (wenn nicht main.py)
# entrypoint = main.py

# (Optional) Architektur festlegen (standard: alle)
# android.archs = arm64-v8a,armeabi-v7a,x86,x86_64

# (Optional) Java/Kotlin Version explizit festlegen (bei Fehlern)
# android.gradle_dependencies = 'com.android.support:appcompat-v7:28.0.0'

# (Optional) Logging & Debug Optionen
log_level = 2
log_enable = True

# (Optional) Umgebungsvariablen setzen
# environment = ENV_VAR=value

# (Optional) Erweiterte Fehlerprotokollierung
# android.logcat_filters = *:S python:D

# (Optional) Splashscreen Einstellungen
# presplash.color = #000000
# presplash.keep = False

# (Optional) App-Verhalten bei Standby
# android.wakelock = False

# (Optional) Extra Python-Optionen
# python.opt = 2

# (Optional) Hook-Skripte (bei komplexen Projekten)
# hooks = hooks/prebuild.sh:before-requirements, hooks/postbuild.sh:after-build

# (Optional) AAB Play Store Upload Settings
# android.upload_apk = False

# (Optional) Günstigere Kompression (kleinere APK)
# android.extra_opts = --compress

###############################################################################
# KEINE weiteren Abschnitte sind für Kivy/Buildozer/Android zwingend notwendig!
# Alles andere (wie [buildozer], [python], [app_android], [app_ios]) ist für
# Spezialfälle und selten nötig. Lass es UNKONFIGURIERT, wenn du es nicht brauchst.
###############################################################################

# (Optional) Buildozer eigene Einstellungen (hier meist leer lassen)
[buildozer]
# log_level = 2
# warn_on_root = 1

# (Optional) Python eigene Einstellungen (hier meist leer lassen)
[python]
# version = 3.11

# (Optional) Android-spezifische Einstellungen (hier meist leer lassen)
[app_android]
# android.allow_backup = 0

# (Optional) iOS-spezifische Einstellungen (hier ignorieren)
[app_ios]
# ios.kivy_ios_url = https://github.com/kivy/kivy-ios

###############################################################################
# FERTIG. Nicht mit Platzhaltern zumüllen!
# App läuft so out-of-the-box durch CI/CD und auf echten Geräten.
###############################################################################