
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class College(Base):
    __tablename__ = 'colleges'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(120), nullable=False)
    address = Column(Text)
    logo_url = Column(Text)

class Student(Base):
    __tablename__ = 'students'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    college_id = Column(UUID(as_uuid=True), ForeignKey('colleges.id'), nullable=False)
    name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    profile_image_url = Column(Text)
    enrollment_number = Column(String(50), unique=True, nullable=False)
    year = Column(Integer)
    branch = Column(String(80))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Activity(Base):
    __tablename__ = 'activities'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey('students.id'), nullable=False)
    name = Column(String(120), nullable=False)
    date = Column(DateTime(timezone=True), nullable=True)
    venue = Column(String(120), nullable=True)
    media_url = Column(Text, nullable=True)
    type = Column(String(50), nullable=True)  # e.g., Certification, Workshop, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
