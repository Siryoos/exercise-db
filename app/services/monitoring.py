import logging
from datetime import datetime
from elasticsearch import Elasticsearch
from prometheus_client import Counter, Histogram
import time
from functools import wraps
from app import es

# تنظیمات لاگینگ
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# متریک‌های Prometheus
request_count = Counter('http_requests_total', 'Total HTTP requests')
request_latency = Histogram('http_request_duration_seconds', 'HTTP request latency')
error_count = Counter('http_errors_total', 'Total HTTP errors')

def log_request(func):
    """دکوراتور برای ثبت درخواست‌ها"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        request_count.inc()
        
        try:
            result = func(*args, **kwargs)
            status_code = result[1] if isinstance(result, tuple) else 200
        except Exception as e:
            error_count.inc()
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise
        finally:
            duration = time.time() - start_time
            request_latency.observe(duration)
            
            # ثبت لاگ در Elasticsearch
            log_data = {
                'timestamp': datetime.now().isoformat(),
                'function': func.__name__,
                'duration': duration,
                'status_code': status_code if 'status_code' in locals() else 500
            }
            
            try:
                es.index(index='api-logs', document=log_data)
            except Exception as e:
                logger.error(f"Error logging to Elasticsearch: {str(e)}")
        
        return result
    return wrapper

def setup_monitoring():
    """راه‌اندازی سیستم مانیتورینگ"""
    # بررسی اتصال به Elasticsearch
    try:
        if not es.ping():
            logger.error("Could not connect to Elasticsearch")
    except Exception as e:
        logger.error(f"Elasticsearch error: {str(e)}")
    
    # ایجاد ایندکس Elasticsearch اگر وجود نداشته باشد
    try:
        es.indices.create(
            index='api-logs',
            ignore=400,  # نادیده گرفتن خطای "ایندکس از قبل وجود دارد"
            body={
                'mappings': {
                    'properties': {
                        'timestamp': {'type': 'date'},
                        'function': {'type': 'keyword'},
                        'duration': {'type': 'float'},
                        'status_code': {'type': 'integer'}
                    }
                }
            }
        )
    except Exception as e:
        logger.error(f"Error creating Elasticsearch index: {str(e)}")

def get_metrics():
    """دریافت متریک‌های سیستم"""
    return {
        'total_requests': request_count._value.get(),
        'total_errors': error_count._value.get(),
        'average_latency': request_latency.observe(0)  # مقدار فعلی هیستوگرام
    }

def log_error(error, context=None):
    """ثبت خطا در سیستم لاگینگ"""
    error_count.inc()
    error_data = {
        'timestamp': datetime.now().isoformat(),
        'error': str(error),
        'context': context or {}
    }
    
    logger.error(f"Error: {str(error)}, Context: {context}")
    
    try:
        es.index(index='api-errors', document=error_data)
    except Exception as e:
        logger.error(f"Error logging to Elasticsearch: {str(e)}")

# راه‌اندازی اولیه سیستم مانیتورینگ
setup_monitoring() 