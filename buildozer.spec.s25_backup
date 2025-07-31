[app]
title = aiDroid
package.name = aidroid
package.domain = org.daydaylx

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,xml

version = 0.1
requirements = python3,kivy==2.3.0,kivymd,requests,sqlite3,android,pyjnius,filetype,cython==0.29.33

[buildozer]
log_level = 2
warn_on_root = 1

[app]
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.3.0

fullscreen = 0
android.presplash_color = #FFFFFF

android.permissions = INTERNET,ACCESS_NETWORK_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,ACCESS_WIFI_STATE

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21
android.private_storage = True
android.add_packaging_options = packagingOptions { pickFirst '**/libc++_shared.so' }

android.gradle_dependencies = 

android.add_gradle_repositories = 

android.archs = arm64-v8a, armeabi-v7a

p4a.branch = master
p4a.bootstrap = sdl2

garden_requirements = 

[buildozer]
bin_dir = /home/user/.buildozer/android/platform/android-sdk/tools/bin
EOF

