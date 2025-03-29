from functools import wraps
import json
from app import redis_client

def cache_response(expire_time=3600):
    """
    دکوراتور برای کش کردن پاسخ‌های API
    
    Args:
        expire_time (int): زمان انقضا به ثانیه (پیش‌فرض: 1 ساعت)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # ساخت کلید کش
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # بررسی وجود نتیجه در کش
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
            
            # اجرای تابع و ذخیره نتیجه در کش
            result = func(*args, **kwargs)
            redis_client.setex(
                name=cache_key,
                time=expire_time,
                value=json.dumps(result)
            )
            return result
        return wrapper
    return decorator

def invalidate_cache(pattern):
    """
    حذف کش‌های منطبق با الگوی مشخص شده
    
    Args:
        pattern (str): الگوی کلید‌های کش برای حذف
    """
    for key in redis_client.scan_iter(pattern):
        redis_client.delete(key)

def cache_set(key, value, expire_time=3600):
    """
    ذخیره مستقیم مقدار در کش
    
    Args:
        key (str): کلید کش
        value (any): مقدار برای ذخیره
        expire_time (int): زمان انقضا به ثانیه
    """
    redis_client.setex(
        name=key,
        time=expire_time,
        value=json.dumps(value)
    )

def cache_get(key):
    """
    دریافت مقدار از کش
    
    Args:
        key (str): کلید کش
    
    Returns:
        any: مقدار ذخیره شده یا None
    """
    value = redis_client.get(key)
    return json.loads(value) if value else None 