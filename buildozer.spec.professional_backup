[app]
title = aiDroid
package.name = aidroid
package.domain = org.daydaylx

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,xml

version = 0.1
requirements = python3==3.9,kivy==2.3.0,kivymd,requests,sqlite3,android,pyjnius,filetype,cython==0.29.33

[buildozer]
log_level = 2
warn_on_root = 1

[app]
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

orientation = portrait
fullscreen = 0
android.presplash_color = #FFFFFF

android.permissions = INTERNET,ACCESS_NETWORK_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,ACCESS_WIFI_STATE,MANAGE_EXTERNAL_STORAGE,READ_MEDIA_IMAGES,READ_MEDIA_VIDEO,READ_MEDIA_AUDIO

android.api = 34
android.minapi = 26
android.sdk = 34
android.ndk = 25b
android.ndk_api = 26
android.private_storage = True

android.archs = arm64-v8a
android.add_packaging_options = packagingOptions { pickFirst '**/libc++_shared.so' }

p4a.branch = master
p4a.bootstrap = sdl2

garden_requirements = 
