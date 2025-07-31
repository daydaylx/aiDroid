[app]
# --------------------------------------------------------
# All gems for a PRODUCTION-READY Kivy/KivyMD Android App
# --------------------------------------------------------

# Basis: Name, Paket, Domain (unique für Play Store!):
title = aiDroid
package.name = aidroid
package.domain = org.daydaylx

# Quellen und Assets (alles was ins APK gehört!):
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,ico,icns,atlas,json,xml,ttf,otf,mp3,mp4,ogg,wav,webm,svg

# Build-Version (auch im Play Store entscheidend):
version = 1.0.0
# Optional: version.code = 100  # <- musst du für Upgrades anpassen!

# Python/Requirements – tested for stability & Play-Store acceptance!
requirements = python3==3.9,kivy==2.3.0,kivymd,requests,sqlite3,android,pyjnius,filetype,cython==0.29.33
# Wenn du z.B. Pillow brauchst: einfach hinzufügen!
# requirements = python3==3.9,kivy==2.3.0,kivymd,requests,sqlite3,android,pyjnius,filetype,cython==0.29.33,pillow

# Garden (Widgets von https://kivy-garden.github.io/ )
#garden_requirements = mapview,graph

# LANDSCAPE Einstellungen (Standard: portrait, meistens gefordert!)
orientation = portrait
fullscreen = 0
android.presplash_color = #FFFFFF

# Icon und Presplash – das wird im Smartphonen-Launcher/Play Store angezeigt:
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

# Sprachunterstützung und Gebiets-Support (locale):
android.supported_locales = en,de,fr,es,ru,zh,jp

# Permissions – MAXIMAL für Medien-/Datei-Nutzung & Internet unter Android 13+:
android.permissions = INTERNET,ACCESS_NETWORK_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,ACCESS_WIFI_STATE,MANAGE_EXTERNAL_STORAGE,READ_MEDIA_IMAGES,READ_MEDIA_VIDEO,READ_MEDIA_AUDIO,FOREGROUND_SERVICE
# For special usecases (camera/scanner): ,CAMERA
# For Geolocation: ,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION

# Share & DeepLinks Support (optional, hier als Beispiel):
#android.manifest.intent_filters = <intent-filter><action android:name="android.intent.action.VIEW"/><category android:name="android.intent.category.DEFAULT"/><category android:name="android.intent.category.BROWSABLE"/></intent-filter>

# File Provider für PDFs/Downloads (nur für File Sharing):
#android.manifest.providers = <provider android:name="androidx.core.content.FileProvider" android:authorities="org.daydaylx.aidroid.fileprovider" android:exported="false" android:grantUriPermissions="true"><meta-data android:name="android.support.FILE_PROVIDER_PATHS" android:resource="@xml/file_paths" /></provider>

# Build-Target, damit dein Code auf neuen Geräten läuft:
android.api = 34        # Android 15 = API 34 (2024, Galaxy S25 etc.)
android.minapi = 26     # Mindestens Android 8 (fast alle Geräte ab 2017!)
android.sdk = 34
android.ndk = 25b       # Noch stabil! p4a empfiehlt 25b (26b noch problematisch)
android.ndk_api = 26

# Speicherort für sensible App-Daten:
android.private_storage = True
# für externen Zugriff (nicht PlayStore-Konform!): False

# CPU Architektur – am Markt üblich bei Snapdragon, Exynos & Mediatek:
android.archs = arm64-v8a
# Tipp: ARMv7 ist zu alt, sollte nicht mehr nötig sein (2025+ only arm64).

# gradle und andere buildtools:
android.gradle_dependencies =
android.add_gradle_repositories =

# Packaging-Workaround für viele moderne native Libs:
android.add_packaging_options = packagingOptions { pickFirst '**/libc++_shared.so' }

# Sprache und Lokalisierung (optional):
#android.accept_language = de

# Kivy-Launcher:
#launcher_icon = %(source.dir)s/icon.png

# p4a (python-for-android): immer "master"-Branch für Stabilität wählen!
p4a.branch = master
p4a.bootstrap = sdl2    # sdl2 ist für fast alle UIs (inkl. KivyMD) optimal!

# ----------- Erweiterte Buildspezifika / Debug / Logging -----------
# Logging für Debugging
log_level = 2

# Root-Warnung (Linux-User mit sudo!)
warn_on_root = 1

# ProGuard für kleinere APKs (PRO und PlayStore, erfordert p4a min. 2022):
#android.use_proguard = 0

# Splash/Custom Permissions (hier leer lassen, wenn nicht notwendig!)
#android.add_src = src/
#android.add_jars =

# Release-Build für den PlayStore (Debug erst final raus, dann auf 1 setzen!)
#android.release = 0

