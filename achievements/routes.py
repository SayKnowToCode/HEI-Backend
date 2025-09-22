from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from db import engine
from models import Achievement, Student
from datetime import datetime

achievements_bp = Blueprint('achievements', __name__)

@achievements_bp.route('/achievements', methods=['POST'])
def add_achievement():
    data = request.get_json()
    student_id = data.get('student_id')
    type_ = data.get('type')
    title = data.get('title')
    description = data.get('description')
    date = data.get('date')
    end_date = data.get('end_date')
    venue = data.get('venue')
    organization = data.get('organization')
    certification_url = data.get('certification_url')
    media_url = data.get('media_url')

    if not student_id or not type_ or not title or not date:
        return jsonify({'error': 'Missing required fields'}), 400

    with Session(engine) as db:
        student = db.query(Student).filter_by(id=student_id).first()
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        achievement = Achievement(
            student_id=student_id,
            type=type_,
            title=title,
            description=description,
            date=datetime.fromisoformat(date),
            end_date=datetime.fromisoformat(end_date) if end_date else None,
            venue=venue,
            organization=organization,
            certification_url=certification_url,
            media_url=media_url,
            status='Pending'
        )
        db.add(achievement)
        db.commit()
        return jsonify({'message': 'Achievement added', 'achievement_id': str(achievement.id)}), 201


@achievements_bp.route('/achievements', methods=['GET'])
def get_achievements():
    student_id = request.args.get('student_id')
    if not student_id:
        return jsonify({'error': 'Missing student_id'}), 400

    with Session(engine) as db:
        achievements = db.query(Achievement).filter_by(student_id=student_id).all()
        print(achievements)
        result = []
        for ach in achievements:
            result.append({
                'id': str(ach.id),
                'type': ach.type,
                'title': ach.title,
                'description': ach.description,
                'date': ach.date.isoformat(),
                'end_date': ach.end_date.isoformat() if ach.end_date else None,
                'venue': ach.venue,
                'organization': ach.organization,
                'certification_url': ach.certification_url,
                'media_url': ach.media_url,
                'status': ach.status,
                'verification_date': ach.verification_date.isoformat() if ach.verification_date else None,
                'verified_by': str(ach.verified_by) if ach.verified_by else None,
                'remarks': ach.remarks
            })
        return jsonify(result), 200