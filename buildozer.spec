[app]

# (str) Title of your application
title = aiDroid S25 Pro

# (str) Package name
package.name = aindroidS25pro

# (str) Package domain (needed for android/ios packaging)
package.domain = org.aiDroid

# (str) App version (method: build.version)
version = 0.0.1

# (list) Application requirements
requirements = python3, kivy, sqlite3

# (list) Application hooks
# The order of execution is:
# - pre-hooks (e.g. before-requirements)
# - build steps (e.g. buildozer android debug)
# - post-hooks (e.g. after-clean)
# Each hook can either be a simple string (the name of a hook) or a more
# complex string like 'hooks/my_custom_hook.sh:before-requirements'.
# For more info, see the buildozer documentation.
# For example:
# hooks = pre-build:my_script.py, post-build:my_other_script.sh
#
# (list) Application source paths
#
# Example:
# source.include_dirs = /path/to/my/extra/files
# source.exclude_dirs = /path/to/my/secret/files
#
# (str) Source code directory
source.dir = .

# (str) The directory where your app's dependencies and assets are stored.
# This is usually the `assets` folder, but can be changed.
# For example:
# source.assets = ./assets

# (str) The directory where your app's libraries are stored.
# This is usually the `libs` folder, but can be changed.
# For example:
# source.libs = ./libs

# (list) Application dependencies (not from PyPI)
# Example:
# source.dependencies = ./my-local-library.zip

# (list) Extra files to be included in the app
# Example:
# source.extra_files = ./data/my-data.json

# (list) Extra folders to be included in the app
# Example:
# source.extra_dirs = ./data

# (str) The path to your icon
# The path must be absolute or relative to the project directory.
icon.filename = %(source.dir)s/icon.png

# (str) The path to your presplash image
presplash.filename = %(source.dir)s/presplash.png

# (list) App permissions (needed for android/ios packaging)
# Example:
# permissions = android.permission.INTERNET, android.permission.WRITE_EXTERNAL_STORAGE
permissions = android.permission.INTERNET, android.permission.ACCESS_NETWORK_STATE

# (str) The Android NDK version to use.
android.ndk_version = 25b

# (str) The Android SDK version to use.
android.sdk_version = 33

# (str) The Android build tools version to use.
android.build_tools_version = 33.0.0

# (str) The Android API level to build against.
android.api = 33

# (bool) Whether to include the Android-specific ProGuard rules.
android.use_proguard = True
android.proguard_rules = proguard-rules.pro

# (list) Android features (permissions) that your app uses.
# Example:
# android.add_a_permissions = android.permission.ACCESS_FINE_LOCATION

# (list) Android activities to be created
# Example:
# android.add_a_activities = org.kivy.MainActivity

# (list) Android services to be created
# Example:
# android.add_a_services = org.kivy.MyService
