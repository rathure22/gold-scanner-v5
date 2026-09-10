[app]
title = Gold Scanner Bisaya
package.name = goldscannerbisaya
package.domain = com.landz.goldscanner
source.dir =.
source.include_exts = py,png,jpg,kv,json
version = 5.0
requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests
orientation = portrait
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 34
android.minapi = 34
android.sdk = 34
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license_agreement = True
p4a.branch = master
p4a.bootstrap = sdl2
[buildozer]
log_level = 1
warn_on_root = 1
