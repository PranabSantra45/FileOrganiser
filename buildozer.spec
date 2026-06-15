[app]

# (str) Title of your application
title = Smart FileFlow

# (str) Package name
package.name = fileflow

# (str) Package domain (needed for android packaging)
package.domain = org.pranabsantra

# (str) Source code directory
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,json,txt

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.2.0,kivymd==1.2.0,pillow,requests,urllib3,certifi,charset_normalizer,idna,pyjnius,android


# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# =============================================================================
# Android specific
# =============================================================================

# (list) Permissions
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE


# (int) Target Android API, should be as high as possible.
android.api = 34


# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25c

# (bool) Use --private data directory (True, default) or --dir public directory (False)
android.private_storage = True

# (str) Android entry point, default is to use start.py
android.entrypoint = main.py

# (list) Pattern to exclude from the data directory
android.exclude_exts = spec, venv, .venv, log, venv/

# (list) List of exclusion patterns for the data directory
android.exclude_dirs = file organiser venv, tests, test_files, .git, .github, .system_generated

# =============================================================================
# Buildozer settings
# =============================================================================

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug and error)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
