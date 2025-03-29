# خزشگر تمرین‌های ورزشی

این پروژه یک خزشگر برای جمع‌آوری اطلاعات تمرین‌های ورزشی از وب‌سایت Bodybuilding.com است. از کتابخانه Crawl4AI برای خزش استفاده می‌کند.

## ویژگی‌ها

- خزش خودکار تمرین‌های ورزشی
- استخراج اطلاعات مهم مانند نام، دسته‌بندی، عضلات درگیر و غیره
- ذخیره نتایج در فرمت JSON
- پشتیبانی از داکر برای اجرای آسان

## پیش‌نیازها

- Docker و Docker Compose
- Python 3.10 یا بالاتر (برای اجرای محلی)

## نصب و راه‌اندازی

1. کلون کردن مخزن:
```bash
git clone https://github.com/yourusername/exercise-crawler.git
cd exercise-crawler
```

2. ساخت و اجرای داکر:
```bash
docker compose build crawler
docker compose run --rm crawler
```

نتایج در پوشه `dist` ذخیره خواهند شد.

## ساختار پروژه

```
exercise-crawler/
├── crawler.py          # کد اصلی خزشگر
├── requirements.txt    # وابستگی‌های پایتون
├── Dockerfile         # تنظیمات داکر
├── docker-compose.yml # تنظیمات داکر کامپوز
└── dist/             # خروجی خزشگر
    └── exercises.json # داده‌های استخراج شده
```

## لایسنس

این پروژه تحت لایسنس MIT منتشر شده است.
