from db import engine

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from db import engine
from sqlalchemy.orm import Session
from models import Student, College, Activity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    enrollment_number = data.get('enrollment_number')
    college_name = data.get('college_name')
    if not email or not password or not name or not enrollment_number or not college_name:
        return jsonify({'error': 'Missing required fields'}), 400
    from sqlalchemy.orm import Session
    with Session(engine) as db:
        try:
            college = db.query(College).filter(College.name == college_name).first()
            if not college:
                return jsonify({'error': 'College not found'}), 404
            student = Student(
                email=email,
                password_hash=generate_password_hash(password),
                name=name,
                enrollment_number=enrollment_number,
                college_id=college.id
            )
            db.add(student)
            db.commit()
            return jsonify({'message': 'User registered successfully'}), 201
        except IntegrityError:
            db.rollback()
            return jsonify({'error': 'User already exists'}), 409

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    from sqlalchemy.orm import Session
    with Session(engine) as db:
        student = db.query(Student).filter_by(email=email).first()
    if not student or not check_password_hash(student.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401
    return jsonify({'message': 'Login successful', 'user_id': str(student.id), 'name': student.name}), 200
    if not student or not check_password_hash(student.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401
    return jsonify({'message': 'Login successful', 'user_id': str(student.id), 'name': student.name}), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logged out'}), 200
