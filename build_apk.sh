#!/bin/bash

# ===========================================
# سكربت بناء APK لتطبيق بلال المحاسبي
# ===========================================

echo "🚀 بدء بناء تطبيق Android..."

# التأكد من تثبيت Flet
pip install flet --upgrade

# بناء APK
echo "📦 جاري إنشاء ملف APK..."
flet build apk \
    --project "بلال المحاسبي البسيط" \
    --org "com.bilal.accountant" \
    --product "BilalAccountant" \
    --build-version "1.0.0"

echo "✅ تم الانتهاء!"
echo "📁 ملف APK موجود في: build/apk/"
