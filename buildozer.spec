[app]
title = Gold Scanner Bisaya
package.name = goldscannerbisaya
package.domain = com.landz.goldscanner
source.dir =.
source.include_exts = py,png,jpg,kv,atlas,json
version = 3.1
requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests
orientation = portrait
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license_agreement = True
p4a.branch = master
[buildozer]
log_level = 1
warn_on_root = 1
