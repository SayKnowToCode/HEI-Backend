from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from sqlalchemy import func, and_, case
from db import engine
from sqlalchemy.orm import Session
from models import Student, College, Achievement, Attendance, Subject, StudentSubject

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'Missing user_id'}), 400
    
    db = Session(engine)
    try:
        # Get student and college info
        student = db.query(Student).filter_by(id=user_id).first()
        if not student:
            return jsonify({'error': 'Student not found'}), 404
            
        # Get current semester subjects and attendance
        current_date = datetime.now()
        academic_year = f"{current_date.year}-{current_date.year + 1}"
        
        # Calculate subject-wise attendance
        subject_attendance = db.query(
            Subject.name.label('subject'),
            func.count().label('total'),
            func.sum(case((Attendance.status == 'Present', 1), else_=0)).label('present')
        ).join(StudentSubject, StudentSubject.subject_id == Subject.id)\
         .join(Attendance, Attendance.subject_id == Subject.id)\
         .filter(
            StudentSubject.student_id == user_id,
            StudentSubject.academic_year == academic_year,
            StudentSubject.is_active == True
         ).group_by(Subject.name).all()
        
        subject_wise = [{
            'subject': subject,
            'total': total,
            'present': present,
            'percentage': (present / total * 100) if total > 0 else 0
        } for subject, total, present in subject_attendance]
        
        # Calculate overall attendance percentage
        overall_attendance = sum(s['present'] for s in subject_wise)
        total_classes = sum(s['total'] for s in subject_wise)
        overall_percentage = (overall_attendance / total_classes * 100) if total_classes > 0 else 0
        
        # Get monthly attendance trend
        thirty_days_ago = current_date - timedelta(days=30)
        monthly_trend = []
        for day in range(30):
            date = thirty_days_ago + timedelta(days=day)
            records = db.query(
                func.count().label('total'),
                func.sum(case((Attendance.status == 'Present', 1), else_=0)).label('present')
            ).filter(
                Attendance.student_id == user_id,
                func.date(Attendance.date) == date.date()
            ).first()
            
            total = records.total or 0
            present = records.present or 0
            monthly_trend.append({
                'date': date.date().isoformat(),
                'present': present,
                'total': total,
                'percentage': (present / total * 100) if total > 0 else 0
            })
        
        # Get recent attendance records
        recent_records = db.query(Attendance).filter(
            Attendance.student_id == user_id
        ).order_by(Attendance.date.desc()).limit(10).all()
        
        recent_records_list = [{
            'date': record.date.isoformat(),
            'subject': record.subject.name,
            'status': record.status,
            'remarks': record.remarks
        } for record in recent_records]
        
        # Get achievements
        achievements = db.query(Achievement).filter_by(student_id=user_id).order_by(Achievement.date.desc()).all()
        achievements_list = [{
            'type': a.type,
            'title': a.title,
            'date': a.date.strftime('%b %Y'),
            'status': a.status,
            'organization': a.organization,
            'certification_url': a.certification_url,
            'media_url': a.media_url
        } for a in achievements]
        
        dashboard_data = {
            'student': {
                'name': student.name,
                'email': student.email,
                'enrollment_number': student.enrollment_number,
                'year': student.year,
                'branch': student.branch,
                'profile_image_url': student.profile_image_url,
                'college': {
                    'id': student.college.id,
                    'name': student.college.name,
                    'logo_url': student.college.logo_url
                }
            },
            'attendance': {
                'overall_percentage': overall_percentage,
                'subject_wise': subject_wise,
                'monthly_trend': monthly_trend,
                'recent_records': recent_records_list
            },
            'analytics': {
                'total_credits': student.total_credits,
                'cgpa': student.cgpa,
                'total_activities': student.total_activities,
                'verified_activities': student.verified_activities,
                'pending_activities': student.pending_activities
            },
            'achievements': achievements_list
        }
        
        return jsonify({'dashboard': dashboard_data}), 200
    
    finally:
        db.close()
