from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
from db import SessionLocal
from models import College

college_auth_bp = Blueprint('college_auth', __name__)

@college_auth_bp.route('/login', methods=['POST'])
def college_login():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')
    db = SessionLocal()
    college = db.query(College).filter_by(name=name).first()
    db.close()
    if not college or not college.password_hash or not check_password_hash(college.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401
    session['college'] = str(college.id)
    return jsonify({'message': 'College login successful', 'college_id': str(college.id), 'name': college.name}), 200

# Route to get logged-in college info
@college_auth_bp.route('/dashboard', methods=['GET'])
def get_college_info():
    college_id = session.get('college')
    if not college_id:
        return jsonify({'error': 'Unauthorized'}), 401
    db = SessionLocal()
    college = db.query(College).filter_by(id=college_id).first()
    db.close()
    if not college:
        return jsonify({'error': 'College not found'}), 404
    return jsonify({
        'college': {
            'id': str(college.id),
            'name': college.name,
            'address': college.address,
            'logo_url': college.logo_url
        }
    }), 200
