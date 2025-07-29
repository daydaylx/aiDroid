[app]
title = OpenRouter CodeGen
package.name = openroutercodegen
package.domain = org.david.codegen

source.dir = .
source.include_exts = py,png,kv,txt

version = 1.0

requirements = python3,kivy,requests,urllib3,certifi

p4a.bootstrap = sdl2
p4a.branch = master

android.permissions = INTERNET
android.api = 30
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
