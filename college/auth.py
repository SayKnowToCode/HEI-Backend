from db import engine
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from db import engine
from sqlalchemy.orm import Session
from models import College

college_auth_bp = Blueprint('college_auth', __name__)

@college_auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')
    from sqlalchemy.orm import Session
    with Session(engine) as db:
        college = db.query(College).filter_by(name=name).first()
    if not college or not college.password_hash or not check_password_hash(college.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401
    return jsonify({'message': 'College login successful', 'college_id': str(college.id), 'name': college.name}), 200
    if not college or not college.password_hash or not check_password_hash(college.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401
    return jsonify({'message': 'College login successful', 'college_id': str(college.id), 'name': college.name}), 200

# Route to get logged-in college info
@college_auth_bp.route('/dashboard', methods=['GET'])
def get_college_info():
    college_id = request.args.get('college_id')
    if not college_id:
        return jsonify({'error': 'Missing college_id'}), 400
    from sqlalchemy.orm import Session
    with Session(engine) as db:
        college = db.query(College).filter_by(id=college_id).first()
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
