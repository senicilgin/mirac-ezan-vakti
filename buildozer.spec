[app]

# -------------------------------------------------
# UYGULAMA BILGILERI
# -------------------------------------------------

title = Miraç Ezan Vakti

# Tam paket adı:
# org.mustafayildiz.ezan
package.name = ezan
package.domain = org.mustafayildiz

# main.py dosyasının bulunduğu klasör
source.dir = .


# -------------------------------------------------
# APK ICINE ALINACAK DOSYALAR
# -------------------------------------------------

source.include_exts = py,kv,png,jpg,jpeg,webp,json,atlas,txt,xml,java,wav,ogg,mp3,m4a,aac

# Gerekli kaynak klasörleri
source.include_patterns = assets/*,assets/**/*,android_res/*,android_res/**/*,ses_kutuphanesi/*,ses_kutuphanesi/**/*

# Derlemeye dahil edilmeyecek klasörler
source.exclude_dirs = .git,.github,__pycache__,bin,.buildozer,.venv,venv,yedek,backup,eski_dosyalar

# Derlemeye dahil edilmeyecek dosyalar
source.exclude_patterns = *.pyc,*.pyo,*_oncesi.py,*_yedek.py,*_backup.py


# -------------------------------------------------
# SURUM BILGISI
# -------------------------------------------------

version = 1.0.0


# -------------------------------------------------
# PYTHON BAGIMLILIKLARI
# -------------------------------------------------

requirements = python3,kivy==2.3.1,plyer,pyjnius


# -------------------------------------------------
# EKRAN AYARLARI
# -------------------------------------------------

orientation = portrait
fullscreen = 0


# -------------------------------------------------
# UYGULAMA IKONU VE ACILIS GORSELI
# -------------------------------------------------

icon.filename = %(source.dir)s/assets/mirac_vakti_icon.png

presplash.filename = %(source.dir)s/assets/mirac_vakti_presplash.png


# -------------------------------------------------
# ANDROID IZINLERI
# -------------------------------------------------

android.permissions = INTERNET,POST_NOTIFICATIONS,VIBRATE,SCHEDULE_EXACT_ALARM,REQUEST_IGNORE_BATTERY_OPTIMIZATIONS,FOREGROUND_SERVICE,FOREGROUND_SERVICE_SPECIAL_USE,RECEIVE_BOOT_COMPLETED


# -------------------------------------------------
# ANDROID API VE NDK AYARLARI
# -------------------------------------------------

# Hedef Android API seviyesi
android.api = 36

# Android 7.0 ve üzeri
# preadv ve pwritev derleme hatası nedeniyle API 24 gereklidir
android.minapi = 24

# Android NDK sürümü
android.ndk = 27c


# -------------------------------------------------
# ISLEMCI MIMARILERI
# -------------------------------------------------

# 64-bit ve 32-bit ARM telefonlar
android.archs = arm64-v8a,armeabi-v7a


# -------------------------------------------------
# ANDROID SDK AYARLARI
# -------------------------------------------------

android.accept_sdk_license = True

android.enable_androidx = True


# -------------------------------------------------
# ANDROIDX JAVA BAGIMLILIGI
# -------------------------------------------------

# AlarmReceiver ve bildirim sınıflarında kullanılan
# androidx.core.app.NotificationCompat için
android.gradle_dependencies = androidx.core:core:1.13.1


# -------------------------------------------------
# JAVA KAYNAKLARI
# -------------------------------------------------

android.add_src = android_src


# -------------------------------------------------
# WIDGET VE ANDROID XML KAYNAKLARI
# -------------------------------------------------

android.add_resources = android_res


# -------------------------------------------------
# LOG AYARLARI
# -------------------------------------------------

android.logcat_filters = *:S python:D


[buildozer]

# Ayrıntılı derleme çıktısı
log_level = 2

# Root kullanımı hakkında uyarı
warn_on_root = 1
