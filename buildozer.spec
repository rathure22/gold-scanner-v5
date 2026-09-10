
[app]
title = Gold Scanner Bisaya
package.name = goldscannerbisaya
package.domain = com.landz.goldscanner
source.dir = .
source.include_exts = py,png,jpg,jpeg,webp,kv,atlas,json
version = 3.1
requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests,urllib3,certifi,charset-normalizer,idna
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.ndk = 26b
android.accept_sdk_license_agreement = True
p4a.bootstrap = sdl2
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 0
