from flask import request, jsonify
from flask_restx import Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import api, limiter
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import os

# تعریف مدل‌های API
login_model = api.model('Login', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

# ایجاد نشست پایگاه داده
engine = create_engine(os.getenv('DATABASE_URL'))
session = Session(engine)

@api.route('/auth/login')
class Login(Resource):
    @limiter.limit("5 per minute")
    @api.expect(login_model)
    def post(self):
        """ورود کاربر و دریافت توکن"""
        username = request.json.get('username')
        password = request.json.get('password')
        
        # در اینجا باید بررسی اعتبار کاربر را انجام دهید
        # این یک مثال ساده است
        if username == "admin" and password == "password":
            access_token = create_access_token(identity=username)
            return {"access_token": access_token}, 200
        
        return {"message": "نام کاربری یا رمز عبور نادرست است"}, 401

@api.route('/auth/protected')
class Protected(Resource):
    @jwt_required()
    def get(self):
        """نمونه endpoint محافظت شده"""
        current_user = get_jwt_identity()
        return {"logged_in_as": current_user}, 200

@api.route('/auth/register')
class Register(Resource):
    @limiter.limit("3 per hour")
    @api.expect(login_model)
    def post(self):
        """ثبت‌نام کاربر جدید"""
        username = request.json.get('username')
        password = request.json.get('password')
        
        # در اینجا باید منطق ثبت‌نام کاربر را پیاده‌سازی کنید
        # این یک مثال ساده است
        hashed_password = generate_password_hash(password)
        
        # ذخیره کاربر در پایگاه داده
        # ...
        
        return {"message": "کاربر با موفقیت ثبت‌نام شد"}, 201

@api.route('/auth/change-password')
class ChangePassword(Resource):
    @jwt_required()
    def post(self):
        """تغییر رمز عبور"""
        current_user = get_jwt_identity()
        old_password = request.json.get('old_password')
        new_password = request.json.get('new_password')
        
        # در اینجا باید منطق تغییر رمز عبور را پیاده‌سازی کنید
        # این یک مثال ساده است
        if old_password == "password":  # بررسی رمز عبور فعلی
            # به‌روزرسانی رمز عبور در پایگاه داده
            # ...
            return {"message": "رمز عبور با موفقیت تغییر کرد"}, 200
        
        return {"message": "رمز عبور فعلی نادرست است"}, 401 