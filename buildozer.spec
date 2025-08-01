[app]

title = aiDroid S25 Pro

package.name = aidroid

package.domain = org.daydaylx

source.dir = .

source.include_exts = py,png,jpg,kv,atlas,json,xml

version = 2.0.0

requirements = python3,kivy,kivymd

icon.filename = %(source.dir)s/icon.png

presplash.filename = %(source.dir)s/presplash.png

orientation = portrait

fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE

android.api = 30

android.minapi = 21

android.ndk = 25b

android.ndk_api = 21

android.private_storage = True

android.archs = arm64-v8a

p4a.bootstrap = sdl2

p4a.branch = master


[buildozer]

log_level = 2

warn_on_root = 1

cython.options = --compiler-directives=language_level=3
