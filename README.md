# 📱 بلال المحاسبي البسيط - تطبيق Python

تطبيق لإدارة حسابات العملاء والديون للبقالات مبني بـ Python + Flet

## 🚀 التشغيل على الكمبيوتر

### 1. تثبيت المتطلبات
```bash
cd python_app
pip install -r requirements.txt
```

### 2. تشغيل التطبيق
```bash
python main.py
```

---

## 📱 إنشاء تطبيق Android (APK)

### الطريقة 1: باستخدام Flet (الأسهل)

```bash
# تثبيت أدوات البناء
pip install flet

# إنشاء APK
flet build apk
```

سيتم إنشاء ملف APK في مجلد `build/apk`

### الطريقة 2: باستخدام Buildozer (للتخصيص الكامل)

#### أ. تثبيت Buildozer
```bash
pip install buildozer
```

#### ب. إنشاء ملف التكوين
```bash
buildozer init
```

#### ج. تعديل buildozer.spec
```ini
[app]
title = بلال المحاسبي
package.name = bilalaccountant
package.domain = com.bilal
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0.0
requirements = python3,flet
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
```

#### د. بناء APK
```bash
buildozer android debug
```

---

## 📱 إنشاء تطبيق iOS

```bash
flet build ipa
```

---

## 🛠️ البناء على الجوال مباشرة

### باستخدام Termux على Android:

```bash
# تثبيت Termux من F-Droid

# تثبيت Python
pkg update
pkg install python

# تثبيت المتطلبات
pip install flet

# تشغيل التطبيق
cd /sdcard/BilalApp
python main.py
```

---

## ✨ مميزات التطبيق

- ✅ إضافة وتعديل وحذف العملاء
- ✅ تسجيل الديون والسدادات
- ✅ سقف المديونية مع تنبيه
- ✅ إرسال تذكير واتساب
- ✅ إرسال SMS
- ✅ تخزين محلي
- ✅ يعمل بدون إنترنت
- ✅ دعم اللغة العربية

---

## 📂 هيكل الملفات

```
python_app/
├── main.py           # الكود الرئيسي
├── requirements.txt  # المتطلبات
├── README.md         # التوثيق
└── bilal_data.json   # ملف البيانات (يُنشأ تلقائياً)
```

---

## 🔧 التخصيص

### تغيير الألوان
في ملف `main.py`:
```python
page.theme = ft.Theme(
    color_scheme_seed=ft.colors.GREEN,  # غير اللون هنا
)
```

### تغيير الأيقونة
عند البناء بـ Flet:
```bash
flet build apk --icon assets/icon.png
```

---

## 📞 الدعم

للأسئلة والاستفسارات، تواصل معنا!
