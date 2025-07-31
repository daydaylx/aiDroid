[app]
# (str) Title of your application
title = aiDroid S25 Pro

# (str) Package name
package.name = aidroid

# (str) Package domain (needed for android/ios packaging)
package.domain = org.daydaylx

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json,xml

# (str) Application versioning (method 1)
version = 2.0.0

# (list) Application requirements
# python3==3.11.5 für bessere Performance
# kivy==2.3.1 neueste stabile Version
# kivymd==2.0.1.dev0 aktuelle Entwicklung
requirements = python3==3.11.5,kivy==2.3.1,kivymd==2.0.1.dev0,requests==2.32.3,pyjnius==1.6.1,cython==3.0.8,sqlite3,android,filetype,cryptography,keyring

# (str) Presplash of the application
presplash.filename = %(source.dir)s/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (landscape, sensorLandscape, portrait, sensorPortrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for android toolchain)
android.presplash_color = #1a1a1a

# (list) Permissions
# Optimiert für Android 15 / Samsung S25
# Scoped Storage kompatibel
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,(name=READ_EXTERNAL_STORAGE;maxSdkVersion=32),(name=WRITE_EXTERNAL_STORAGE;maxSdkVersion=29),READ_MEDIA_IMAGES,READ_MEDIA_VIDEO,READ_MEDIA_AUDIO

# (int) Target Android API, should be as high as possible.
# Android 15 für Galaxy S25
android.api = 35

# (int) Minimum API your APK / AAB will support.
# Android 10+ für bessere Kompatibilität
android.minapi = 29

# (str) Android NDK version to use
# Neueste stabile Version
android.ndk = 26b

# (int) Android NDK API to use. This is the minimum API your app will support
android.ndk_api = 29

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android arch to build for
# Nur ARM64 für S25 (Snapdragon 8 Elite)
android.archs = arm64-v8a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) XML file for Android network security config
android.network_security_config = network_config.xml

# (str) Bootstrap to use for android builds
p4a.bootstrap = sdl2

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
p4a.arch = arm64-v8a

# (str) python-for-android branch to use
p4a.branch = master

# Performance & Size Optimizations
android.enable_androidx = True
android.minifyEnabled = True
android.shrinkResources = True

# Gradle dependencies for optimization
android.gradle_dependencies = 

# Gradle repositories
android.add_gradle_repositories = 

# Additional packaging options
android.add_packaging_options = packagingOptions { 
    pickFirst '**/libc++_shared.so'
    exclude 'META-INF/LICENSE'
    exclude 'META-INF/NOTICE'
    exclude 'META-INF/DEPENDENCIES'
}

# ProGuard rules file
android.proguard_file = proguard-rules.pro

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
