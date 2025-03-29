# پایگاه داده تمرین‌های ورزشی

این پروژه یک API جامع برای مدیریت تمرین‌های ورزشی است که شامل اطلاعات دقیق در مورد تمرین‌ها، عضلات درگیر، دستورالعمل‌ها و تصاویر مربوطه می‌باشد.

## ویژگی‌ها

- مدیریت کامل تمرین‌ها (CRUD)
- سیستم احراز هویت با JWT
- کش‌گذاری با Redis
- مانیتورینگ و لاگینگ با Elasticsearch و Prometheus
- مستندسازی API با Swagger
- محدودیت نرخ درخواست (Rate Limiting)
- پشتیبانی از حالت آفلاین
- بهینه‌سازی عملکرد

## پیش‌نیازها

- Python 3.8+
- PostgreSQL
- Redis
- Elasticsearch
- Node.js (برای فرانت‌اند)

## نصب و راه‌اندازی

1. کلون کردن مخزن:
```bash
git clone https://github.com/siryoos/exercise-db.git
cd exercise-db
```

2. ایجاد محیط مجازی Python:
```bash
python -m venv venv
source venv/bin/activate  # در لینوکس/مک
venv\Scripts\activate  # در ویندوز
```

3. نصب وابستگی‌ها:
```bash
pip install -r requirements.txt
```

4. تنظیم فایل .env:
```bash
cp .env.example .env
# ویرایش فایل .env و تنظیم مقادیر مناسب
```

5. راه‌اندازی پایگاه داده:
```bash
flask db upgrade
```

6. اجرای برنامه:
```bash
flask run
```

## ساختار پروژه

```
exercise-db/
├── app/
│   ├── models/
│   │   └── models.py
│   ├── routes/
│   │   ├── exercise_routes.py
│   │   └── auth_routes.py
│   ├── services/
│   │   ├── cache_service.py
│   │   └── monitoring.py
│   └── __init__.py
├── migrations/
├── tests/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## API Endpoints

### تمرین‌ها
- `GET /api/exercises` - دریافت لیست تمرین‌ها
- `POST /api/exercises` - ایجاد تمرین جدید
- `GET /api/exercises/<id>` - دریافت جزئیات تمرین
- `PUT /api/exercises/<id>` - به‌روزرسانی تمرین
- `DELETE /api/exercises/<id>` - حذف تمرین
- `GET /api/exercises/search` - جستجو در تمرین‌ها

### احراز هویت
- `POST /api/auth/login` - ورود کاربر
- `POST /api/auth/register` - ثبت‌نام کاربر جدید
- `POST /api/auth/change-password` - تغییر رمز عبور

## مستندات API

مستندات کامل API در آدرس `/api/docs` قابل دسترسی است.

## تست‌ها

برای اجرای تست‌ها:
```bash
pytest
```

برای اجرای تست‌های عملکرد:
```bash
locust -f tests/performance/locustfile.py
```

## مشارکت

1. Fork کردن پروژه
2. ایجاد شاخه برای ویژگی جدید
3. Commit کردن تغییرات
4. Push کردن به شاخه
5. ایجاد Pull Request

## لایسنس

این پروژه تحت لایسنس MIT منتشر شده است.
