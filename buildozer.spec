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
# STABLE VERSIONS - tested and working
requirements = python3==3.10.12,kivy==2.2.2,kivymd

# (str) Presplash of the application
presplash.filename = %(source.dir)s/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (landscape, sensorLandscape, portrait, sensorPortrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for android toolchain)
android.presplash_color = #1565C0

# (list) Permissions - MINIMAL for stable build
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 32

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support
android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) Bootstrap to use for android builds
p4a.bootstrap = sdl2

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
p4a.arch = arm64-v8a

# (str) python-for-android branch to use
p4a.branch = master

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
