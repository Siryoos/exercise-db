from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import os

Base = declarative_base()

class Exercise(Base):
    __tablename__ = 'exercises'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    force = Column(String(50))
    level = Column(String(50), nullable=False)
    mechanic = Column(String(50))
    equipment = Column(String(100))
    category = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    muscles = relationship('ExerciseMuscle', back_populates='exercise')
    instructions = relationship('ExerciseInstruction', back_populates='exercise')
    images = relationship('ExerciseImage', back_populates='exercise')

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