from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import os
from app import db

Base = declarative_base()

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    force = db.Column(db.String(50), nullable=True)
    level = db.Column(db.String(50), nullable=False)
    mechanic = db.Column(db.String(50), nullable=True)
    equipment = db.Column(db.String(50), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    primary_muscles = db.Column(db.JSON, nullable=False)
    secondary_muscles = db.Column(db.JSON, nullable=False)
    instructions = db.Column(db.JSON, nullable=False)
    images = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'force': self.force,
            'level': self.level,
            'mechanic': self.mechanic,
            'equipment': self.equipment,
            'category': self.category,
            'primaryMuscles': self.primary_muscles,
            'secondaryMuscles': self.secondary_muscles,
            'instructions': self.instructions,
            'images': self.images,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Muscle(Base):
    __tablename__ = 'muscles'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)  # primary/secondary
    
    exercises = relationship('ExerciseMuscle', back_populates='muscle')

class ExerciseMuscle(Base):
    __tablename__ = 'exercise_muscles'
    
    exercise_id = Column(Integer, ForeignKey('exercises.id'), primary_key=True)
    muscle_id = Column(Integer, ForeignKey('muscles.id'), primary_key=True)
    
    exercise = relationship('Exercise', back_populates='muscles')
    muscle = relationship('Muscle', back_populates='exercises')

class ExerciseInstruction(Base):
    __tablename__ = 'exercise_instructions'
    
    id = Column(Integer, primary_key=True)
    exercise_id = Column(Integer, ForeignKey('exercises.id'))
    instruction = Column(Text, nullable=False)
    order_index = Column(Integer, nullable=False)
    
    exercise = relationship('Exercise', back_populates='instructions')

class ExerciseImage(Base):
    __tablename__ = 'exercise_images'
    
    id = Column(Integer, primary_key=True)
    exercise_id = Column(Integer, ForeignKey('exercises.id'))
    image_url = Column(String(255), nullable=False)
    order_index = Column(Integer, nullable=False)
    
    exercise = relationship('Exercise', back_populates='images')

# ایجاد اتصال به پایگاه داده
engine = create_engine(os.getenv('DATABASE_URL'))

# ایجاد جداول
def init_db():
    Base.metadata.create_all(engine) 