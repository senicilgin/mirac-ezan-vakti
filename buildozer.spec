[app]

title = Miraç Ezan Vakti

package.name = ezan
package.domain = org.mustafayildiz

source.dir = .

source.include_exts = py,png,jpg,jpeg,kv,json,atlas,wav,ogg,mp3,m4a,aac,xml,java

source.exclude_dirs = .git,__pycache__,bin,.buildozer,yedek,backup,eski_dosyalar

version = 1.0.0

requirements = python3,kivy,plyer,pyjnius,androidx.core:core:1.13.1

orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/assets/mirac_vakti_icon.png
presplash.filename = %(source.dir)s/assets/mirac_vakti_presplash.png

icon.adaptive_foreground.filename = %(source.dir)s/assets/mirac_vakti_icon_foreground.png
icon.adaptive_background.filename = %(source.dir)s/assets/mirac_vakti_icon_background.png

android.permissions = INTERNET,POST_NOTIFICATIONS,VIBRATE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,SCHEDULE_EXACT_ALARM,REQUEST_IGNORE_BATTERY_OPTIMIZATIONS,FOREGROUND_SERVICE,FOREGROUND_SERVICE_SPECIAL_USE,RECEIVE_BOOT_COMPLETED

android.api = 36
android.minapi = 23

android.ndk = 27c

android.archs = arm64-v8a, armeabi-v7a

android.accept_sdk_license = True
android.enable_androidx = True

android.add_src = android_src
android.add_resources = android_res

android.logcat_filters = *:S python:D

[buildozer]

log_level = 2
warn_on_root = 1