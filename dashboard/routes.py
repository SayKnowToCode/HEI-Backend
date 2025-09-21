from flask import Blueprint, jsonify, session
from db import SessionLocal
from models import Student, Activity, College

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    user_id = session.get('user')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401
    db = SessionLocal()
    student = db.query(Student).filter_by(id=user_id).first()
    if not student:
        db.close()
        return jsonify({'error': 'Student not found'}), 404
    college = db.query(College).filter_by(id=student.college_id).first()
    activities = db.query(Activity).filter_by(student_id=user_id).all()
    activities_list = [
        {
            'name': a.name,
            'date': a.date.isoformat() if a.date else None,
            'venue': a.venue,
            'media_url': a.media_url,
            'type': a.type
        } for a in activities
    ]
    dashboard_data = {
        'student': {
            'name': student.name,
            'email': student.email,
            'enrollment_number': student.enrollment_number,
            'year': student.year,
            'branch': student.branch,
            'profile_image_url': student.profile_image_url,
            'college': {
                'id': college.id if college else None,
                'name': college.name if college else None,
                'logo_url': college.logo_url if college else None
            }
        },
        'activities': activities_list
    }
    db.close()
    return jsonify({'dashboard': dashboard_data}), 200
