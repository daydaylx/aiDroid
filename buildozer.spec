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

# (list) Application requirements - SIMPLIFIED for stable build
requirements = python3==3.11,kivy==2.3.0,kivymd

# (str) Presplash of the application
presplash.filename = %(source.dir)s/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color
android.presplash_color = #1a1a2a

# (list) Permissions - MINIMAL for first build
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (int) Target Android API - STABLE VERSION
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 26

# (str) Android NDK version to use - RECOMMENDED by P4A
android.ndk = 25b

# (int) Android NDK API to use
android.ndk_api = 26

# (bool) Use --private data storage
android.private_storage = True

# (str) Android archs to build for - SINGLE ARCH for faster build
android.archs = arm64-v8a

# (str) Bootstrap to use for android builds
p4a.bootstrap = sdl2

# (str) python-for-android branch to use
p4a.branch = master

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
