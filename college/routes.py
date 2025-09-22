from db import engine

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from db import engine
from sqlalchemy.orm import Session
from models import College

college_bp = Blueprint('college', __name__)

@college_bp.route('/add', methods=['POST'])
def add_college():
    data = request.get_json()
    name = data.get('name')
    address = data.get('address')
    logo_url = data.get('logo_url')
    password = data.get('password')
    if not name or not password:
        return jsonify({'error': 'College name and password are required'}), 400
    from sqlalchemy.orm import Session
    with Session(engine) as db:
        try:
            password_hash = generate_password_hash(password)
            college = College(name=name, address=address, logo_url=logo_url, password_hash=password_hash)
            db.add(college)
            db.commit()
            return jsonify({'message': 'College added successfully', 'id': str(college.id)}), 201
        except Exception as e:
            db.rollback()
            return jsonify({'error': str(e)}), 500
