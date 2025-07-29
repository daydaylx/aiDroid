[app]
title = OpenRouter CodeGen
package.name = openroutercodegen
package.domain = org.david.codegen

source.dir = .
source.include_exts = py,png,kv,txt

version = 1.0
requirements = python3==3.11,kivy==2.1.0,requests==2.31.0,urllib3==1.26.16,certifi==2023.7.22

p4a.bootstrap = sdl2
p4a.branch = develop
p4a.local_recipes = 

android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
