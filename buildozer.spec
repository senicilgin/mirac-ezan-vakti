[app]

# Uygulamanın görünen adı
title = Miraç Ezan Vakti

# Android paket kimliği:
# org.mustafayildiz.ezan
package.name = ezan
package.domain = org.mustafayildiz

# main.py dosyasının bulunduğu klasör
source.dir = .

# APK içine alınacak dosya uzantıları
source.include_exts = py,png,jpg,jpeg,webp,kv,json,atlas,wav,ogg,mp3,m4a,aac,xml,java,txt

# Derlemeye alınmayacak klasörler
source.exclude_dirs = .git,.github,__pycache__,bin,.buildozer,.venv,venv,yedek,backup,eski_dosyalar

# Derlemeye alınmayacak geçici dosyalar
source.exclude_patterns = *.pyc,*.pyo,*_oncesi.py,*_yedek.py,*_backup.py

# Uygulama sürümü
version = 1.0.0

# Python bağımlılıkları
# AndroidX burada bulunmamalıdır.
requirements = python3,kivy,plyer,pyjnius

# Ekran ayarları
orientation = portrait
fullscreen = 0

# Uygulama ikonu ve açılış görseli
icon.filename = %(source.dir)s/assets/mirac_vakti_icon.png
presplash.filename = %(source.dir)s/assets/mirac_vakti_presplash.png

# Android adaptif ikonları
icon.adaptive_foreground.filename = %(source.dir)s/assets/mirac_vakti_icon_foreground.png
icon.adaptive_background.filename = %(source.dir)s/assets/mirac_vakti_icon_background.png

# Android izinleri
# Rahatsız Etmeyin erişimi kaldırılmıştır.
android.permissions = INTERNET,POST_NOTIFICATIONS,VIBRATE,SCHEDULE_EXACT_ALARM,REQUEST_IGNORE_BATTERY_OPTIMIZATIONS,FOREGROUND_SERVICE,FOREGROUND_SERVICE_SPECIAL_USE,RECEIVE_BOOT_COMPLETED

# Android API ayarları
android.api = 36
android.minapi = 23
android.ndk = 27c

# Desteklenecek telefon işlemci mimarileri
android.archs = arm64-v8a,armeabi-v7a

# Android SDK lisanslarını kabul et
android.accept_sdk_license = True

# AndroidX desteği
android.enable_androidx = True

# Java tarafından kullanılan AndroidX NotificationCompat bağımlılığı
android.gradle_dependencies = androidx.core:core:1.13.1

# Özel Java kaynakları
android.add_src = android_src

# Widget ve diğer Android XML kaynakları
android.add_resources = android_res

# Android log çıktısı
android.logcat_filters = *:S python:D

# Python tarafından kullanılan Java API'lerinin korunması
android.proguard_rules = -keep class org.mustafayildiz.ezan.** { *; }

# Debug APK için optimizasyon
android.debug_artifact = apk

[buildozer]

# Ayrıntılı derleme çıktısı
log_level = 2

# Root kullanıcı uyarısı
warn_on_root = 1
