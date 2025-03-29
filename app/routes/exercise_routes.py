from flask import request
from flask_restx import Resource, fields
from app import api, limiter
from app.models.models import Exercise, Muscle, ExerciseMuscle, ExerciseInstruction, ExerciseImage
from app.services.cache_service import cache_response
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import os

# تعریف مدل‌های API
muscle_model = api.model('Muscle', {
    'id': fields.Integer,
    'name': fields.String,
    'type': fields.String
})

instruction_model = api.model('Instruction', {
    'id': fields.Integer,
    'instruction': fields.String,
    'order_index': fields.Integer
})

image_model = api.model('Image', {
    'id': fields.Integer,
    'image_url': fields.String,
    'order_index': fields.Integer
})

exercise_model = api.model('Exercise', {
    'id': fields.Integer,
    'name': fields.String,
    'force': fields.String,
    'level': fields.String,
    'mechanic': fields.String,
    'equipment': fields.String,
    'category': fields.String,
    'muscles': fields.List(fields.Nested(muscle_model)),
    'instructions': fields.List(fields.Nested(instruction_model)),
    'images': fields.List(fields.Nested(image_model))
})

# ایجاد نشست پایگاه داده
engine = create_engine(os.getenv('DATABASE_URL'))
session = Session(engine)

@api.route('/exercises')
class ExerciseList(Resource):
    @limiter.limit("5 per minute")
    @cache_response(expire_time=300)  # کش برای 5 دقیقه
    @api.marshal_list_with(exercise_model)
    def get(self):
        """دریافت لیست تمام تمرین‌ها"""
        exercises = session.query(Exercise).all()
        return exercises

    @api.expect(exercise_model)
    @api.marshal_with(exercise_model)
    def post(self):
        """ایجاد تمرین جدید"""
        data = request.json
        exercise = Exercise(
            name=data['name'],
            force=data.get('force'),
            level=data['level'],
            mechanic=data.get('mechanic'),
            equipment=data.get('equipment'),
            category=data['category']
        )
        session.add(exercise)
        session.commit()
        return exercise, 201

@api.route('/exercises/<int:id>')
class ExerciseDetail(Resource):
    @cache_response(expire_time=300)
    @api.marshal_with(exercise_model)
    def get(self, id):
        """دریافت جزئیات یک تمرین خاص"""
        exercise = session.query(Exercise).get_or_404(id)
        return exercise

    @api.expect(exercise_model)
    @api.marshal_with(exercise_model)
    def put(self, id):
        """به‌روزرسانی یک تمرین"""
        exercise = session.query(Exercise).get_or_404(id)
        data = request.json
        
        for key, value in data.items():
            if hasattr(exercise, key):
                setattr(exercise, key, value)
        
        session.commit()
        return exercise

    def delete(self, id):
        """حذف یک تمرین"""
        exercise = session.query(Exercise).get_or_404(id)
        session.delete(exercise)
        session.commit()
        return '', 204

@api.route('/exercises/search')
class ExerciseSearch(Resource):
    @cache_response(expire_time=300)
    @api.marshal_list_with(exercise_model)
    def get(self):
        """جستجو در تمرین‌ها"""
        query = request.args.get('q', '')
        category = request.args.get('category')
        level = request.args.get('level')
        
        filters = []
        if query:
            filters.append(Exercise.name.ilike(f'%{query}%'))
        if category:
            filters.append(Exercise.category == category)
        if level:
            filters.append(Exercise.level == level)
        
        exercises = session.query(Exercise).filter(*filters).all()
        return exercises 