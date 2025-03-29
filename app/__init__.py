from flask import Flask
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from redis import Redis
from elasticsearch import Elasticsearch
from prometheus_client import Counter, Histogram
import os
from dotenv import load_dotenv

import werkzeug
if not hasattr(werkzeug, '__version__'):
    werkzeug.__version__ = "2.2.2"

load_dotenv()

app = Flask(__name__)

# تنظیمات پایگاه داده
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/exercise_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-here')

# تنظیم SQLAlchemy
db = SQLAlchemy(app)

# تنظیم Flask-Migrate
migrate = Migrate(app, db)

# تنظیم JWT
jwt = JWTManager(app)

# تنظیم Redis
redis_client = Redis.from_url(os.getenv('REDIS_URL', 'redis://redis:6379/0'))

# تنظیم Elasticsearch
es = Elasticsearch([os.getenv('ELASTICSEARCH_URL', 'http://es:9200')])

# تنظیم Rate Limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# تنظیم Prometheus metrics
request_count = Counter('http_requests_total', 'Total HTTP requests')
request_latency = Histogram('http_request_duration_seconds', 'HTTP request latency')

# Import routes after all configurations
from app.routes import exercise_routes, auth_routes, health_routes

# تنظیم API بعد از import کردن routes
from flask_restx import Api
api = Api(
    app,
    version='1.0',
    title='Exercise API',
    description='API for managing exercises',
    doc='/api/docs'
)

if __name__ == '__main__':
    app.run(debug=True) 