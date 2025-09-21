
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(120), nullable=False)
    credits = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    students = relationship("StudentSubject", back_populates="subject")

class StudentSubject(Base):
    __tablename__ = 'student_subjects'
    student_id = Column(UUID(as_uuid=True), ForeignKey('students.id'), primary_key=True)
    subject_id = Column(UUID(as_uuid=True), ForeignKey('subjects.id'), primary_key=True)
    semester = Column(Integer, nullable=False)
    academic_year = Column(String(9), nullable=False)  # Format: 2024-2025
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student = relationship("Student", back_populates="enrollments")
    subject = relationship("Subject", back_populates="students")

class College(Base):
    __tablename__ = 'colleges'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(120), nullable=False)
    address = Column(Text)
    logo_url = Column(Text)
<<<<<<< Updated upstream
    students = relationship("Student", back_populates="college")
    faculty = relationship("Faculty", back_populates="college")

class Faculty(Base):
    __tablename__ = 'faculty'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    college_id = Column(UUID(as_uuid=True), ForeignKey('colleges.id'), nullable=False)
    name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    department = Column(String(80), nullable=False)
    designation = Column(String(80), nullable=False)
    profile_image_url = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    college = relationship("College", back_populates="faculty")
    verified_achievements = relationship("Achievement", back_populates="verifier")

class Achievement(Base):
    __tablename__ = 'achievements'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey('students.id'), nullable=False)
    type = Column(String(50), nullable=False)  # Certification, Competition, Workshop, Club, Volunteering, Internship
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)  # For activities with duration
    venue = Column(String(120), nullable=True)
    organization = Column(String(120), nullable=True)
    certification_url = Column(Text, nullable=True)
    media_url = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default='Pending')  # Verified, Pending, Rejected
    verification_date = Column(DateTime(timezone=True), nullable=True)
    verified_by = Column(UUID(as_uuid=True), ForeignKey('faculty.id'), nullable=True)
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student = relationship("Student", back_populates="achievements")
    verifier = relationship("Faculty", back_populates="verified_achievements")

class Attendance(Base):
    __tablename__ = 'attendance'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey('students.id'), nullable=False)
    subject_id = Column(UUID(as_uuid=True), ForeignKey('subjects.id'), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(20), nullable=False)  # Present, Absent, Late
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student = relationship("Student", back_populates="attendances")
    subject = relationship("Subject", backref="attendances")
=======
    password_hash = Column(Text, nullable=True)  # For college login
>>>>>>> Stashed changes

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
    
    # Analytics fields
    total_credits = Column(Integer, default=0)
    cgpa = Column(Float, default=0.0)
    total_activities = Column(Integer, default=0)
    verified_activities = Column(Integer, default=0)
    pending_activities = Column(Integer, default=0)
    
    # Relationships
    achievements = relationship("Achievement", back_populates="student")
    attendances = relationship("Attendance", back_populates="student")
    enrollments = relationship("StudentSubject", back_populates="student")
    college = relationship("College", back_populates="students")

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
