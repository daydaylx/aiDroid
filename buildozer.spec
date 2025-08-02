[app]

# (str) Title of your application
[cite_start]title = aiDroid S25 Pro [cite: 38]

# (str) Package name
[cite_start]package.name = aindroidS25pro [cite: 38]

# (str) Package domain (needed for android/ios packaging)
[cite_start]package.domain = org.aiDroid [cite: 38]

# (str) App version (method: build.version)
[cite_start]version = 0.0.1 [cite: 38]

# (list) Application requirements
[cite_start]requirements = python3, kivy, sqlite3 [cite: 38]

# (list) Application hooks
# The order of execution is:
# - pre-hooks (e.g. before-requirements)
# - build steps (e.g. buildozer android debug)
# - post-hooks (e.g. after-clean)
# Each hook can either be a simple string (the name of a hook) or a more
# [cite_start]complex string like 'hooks/my_custom_hook.sh:before-requirements'. [cite: 38]
# [cite_start]For more info, see the buildozer documentation. [cite: 39]
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
[cite_start]source.dir = . [cite: 39]

# (str) [cite_start]The directory where your app's dependencies and assets are stored. [cite: 40]
# [cite_start]This is usually the `assets` folder, but can be changed. [cite: 41]
# For example:
# source.assets = ./assets

# (str) [cite_start]The directory where your app's libraries are stored. [cite: 43]
# [cite_start]This is usually the `libs` folder, but can be changed. [cite: 44]
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
[cite_start]icon.filename = %(source.dir)s/icon.png [cite: 45]

# (str) The path to your presplash image
[cite_start]presplash.filename = %(source.dir)s/presplash.png [cite: 45]

# (list) App permissions (needed for android/ios packaging)
# Example:
# permissions = android.permission.INTERNET, android.permission.WRITE_EXTERNAL_STORAGE
[cite_start]permissions = android.permission.INTERNET, android.permission.ACCESS_NETWORK_STATE [cite: 45]

# (str) The Android NDK version to use.
[cite_start]android.ndk_version = 25b [cite: 46]

# (str) The Android SDK version to use.
[cite_start]android.sdk_version = 33 [cite: 47]

# (str) The Android build tools version to use.
[cite_start]android.build_tools_version = 33.0.0 [cite: 48]

# (str) The Android API level to build against.
[cite_start]android.api = 33 [cite: 49]

# (bool) If True, automatically accept SDK license agreements.
android.accept_sdk_license = True

# (bool) Whether to include the Android-specific ProGuard rules.
[cite_start]android.use_proguard = True [cite: 50]
[cite_start]android.proguard_rules = proguard-rules.pro [cite: 50]

# (list) [cite_start]Android features (permissions) that your app uses. [cite: 51]
# Example:
# android.add_a_permissions = android.permission.ACCESS_FINE_LOCATION

# (list) Android activities to be created
# Example:
# android.add_a_activities = org.kivy.MainActivity

# (list) Android services to be created
# Example:
# android.add_a_services = org.kivy.MyService
