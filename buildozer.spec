[app]
title             = OpenRouter CodeGen
package.name       = openroutercodegen
package.domain     = org.david.codegen

source.dir         = .
source.include_exts = py,kv,png,ttf,txt

version            = 1.1

requirements       = \
    python3==3.11.5,\
    kivy==2.3.1,\
    hostpython3==3.11.5,\
    cython==0.29.36,\
    requests==2.31.0,\
    urllib3==1.26.16,\
    certifi==2023.7.22

p4a.bootstrap      = sdl2
p4a.branch         = develop
p4a.hostpython     = 3.11.5

android.api        = 35
android.minapi     = 24
android.ndk        = 26b
android.ndk_api    = 24
android.permissions = INTERNET
android.archs      = arm64-v8a

android.network_security_config = network_config.xml

orientation        = portrait
fullscreen         = 0

[buildozer]
log_level          = 2
warn_on_root       = 1
