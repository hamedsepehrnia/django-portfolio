# راهنمای راه‌اندازی سیستم ترجمه

سیستم ترجمه با استفاده از `django-modeltranslation` و i18n داخلی Django پیاده‌سازی شده است.

## مراحل راه‌اندازی

### 1. نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```

### 2. اجرای مایگریشن‌ها

بعد از نصب `django-modeltranslation`، باید مایگریشن‌های جدید را ایجاد و اجرا کنید:

```bash
python manage.py makemigrations
python manage.py migrate
```

این دستورات فیلدهای ترجمه (مثل `title_en`, `title_fa`, `description_en`, `description_fa` و ...) را به جداول اضافه می‌کنند.

### 3. ایجاد فایل‌های ترجمه

برای ترجمه متن‌های استاتیک در تمپلیت‌ها:

```bash
# ایجاد فایل‌های ترجمه
python manage.py makemessages -l fa
python manage.py makemessages -l en
```

این دستورات فایل‌های `.po` را در پوشه `locale/fa/LC_MESSAGES/` و `locale/en/LC_MESSAGES/` ایجاد می‌کنند.

### 4. ترجمه متن‌ها

فایل `locale/fa/LC_MESSAGES/django.po` را باز کنید و ترجمه‌های فارسی را اضافه کنید:

```po
msgid "Home"
msgstr "خانه"

msgid "About"
msgstr "درباره ما"

msgid "Services"
msgstr "خدمات ما"

# و غیره...
```

### 5. کامپایل ترجمه‌ها

بعد از ترجمه، فایل‌های `.po` را کامپایل کنید:

```bash
python manage.py compilemessages
```

### 6. استفاده در ادمین

در پنل ادمین Django، برای هر مدل (Hero, About, Service, PortfolioItem) تب‌های زبان (English/Farsi) نمایش داده می‌شود و می‌توانید محتوا را برای هر زبان جداگانه وارد کنید.

## نکات مهم

- محتوای مدل‌ها (Hero, About, Service, PortfolioItem) باید در پنل ادمین برای هر زبان جداگانه وارد شود
- متن‌های استاتیک در تمپلیت‌ها با استفاده از `{% trans %}` ترجمه می‌شوند
- URL ها به صورت `/en/` و `/fa/` هستند (زبان پیش‌فرض بدون prefix است)
- برای تغییر زبان، از دکمه زبان در منوی ناوبری استفاده کنید

