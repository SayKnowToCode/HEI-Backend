
from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from db import SessionLocal
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
    profile_image_url = data.get('profile_image_url')
    year = data.get('year')
    branch = data.get('branch')
    # Activities: conferences, certifications, clubs, competitions, leadership, community
    activity_keys = ['conferences', 'certifications', 'clubs', 'competitions', 'leadership', 'community']
    activities_payload = []
    for key in activity_keys:
        entries = data.get(key, [])
        if isinstance(entries, list):
            for entry in entries:
                # entry can be {name, date, venue, media_url} or {name, date, venue, media}
                activity = {
                    'name': entry.get('name', '') if isinstance(entry, dict) else str(entry),
                    'type': key.capitalize(),
                    'media_url': entry.get('media_url') if isinstance(entry, dict) and entry.get('media_url') else None,
                    'date': entry.get('date') if isinstance(entry, dict) and entry.get('date') else None,
                    'venue': entry.get('venue') if isinstance(entry, dict) and entry.get('venue') else None,
                }
                activities_payload.append(activity)

    if not email or not password or not name or not enrollment_number or not college_name:
        return jsonify({'error': 'Missing required fields'}), 400
    db = SessionLocal()
    try:
        # Find college by name
        college = db.query(College).filter(College.name == college_name).first()
        if not college:
            return jsonify({'error': 'College not found'}), 404
        student = Student(
            email=email,
            password_hash=generate_password_hash(password),
            name=name,
            enrollment_number=enrollment_number,
            college_id=college.id,
            profile_image_url=profile_image_url,
            year=year,
            branch=branch
        )
        db.add(student)
        db.flush()  # Get student.id before commit
        # Save activities
        for act in activities_payload:
            activity = Activity(
                student_id=student.id,
                name=act['name'],
                type=act['type'],
                media_url=act['media_url'],
                date=act['date'],
                venue=act['venue']
            )
            db.add(activity)
        db.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except IntegrityError:
        db.rollback()
        return jsonify({'error': 'User already exists'}), 409
    finally:
        db.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    db = SessionLocal()
    student = db.query(Student).filter_by(email=email).first()
    db.close()
    if not student or not check_password_hash(student.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401
    session['user'] = str(student.id)
    return jsonify({'message': 'Login successful', 'user_id': str(student.id), 'name': student.name}), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({'message': 'Logged out'}), 200
