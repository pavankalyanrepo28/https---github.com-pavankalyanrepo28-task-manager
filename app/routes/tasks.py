from flask import Blueprint, request, jsonify
from app.models import Task, TaskShare, Attachment, Category, User
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import os
from werkzeug.utils import secure_filename

bp = Blueprint('tasks', __name__)

@bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'created_at': task.created_at.isoformat(),
        'due_date': task.due_date.isoformat() if task.due_date else None,
        'completed': task.completed
    } for task in tasks]), 200

@bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    task = Task(
        title=data['title'],
        description=data.get('description'),
        due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None,
        user_id=user_id
    )
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'created_at': task.created_at.isoformat(),
        'due_date': task.due_date.isoformat() if task.due_date else None,
        'completed': task.completed
    }), 201

@bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    task.due_date = datetime.fromisoformat(data['due_date']) if data.get('due_date') else task.due_date
    
    db.session.commit()
    
    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'created_at': task.created_at.isoformat(),
        'due_date': task.due_date.isoformat() if task.due_date else None,
        'completed': task.completed
    }), 200

@bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'message': 'Task deleted successfully'}), 200

@bp.route('/tasks/shared', methods=['GET'])
@jwt_required()
def get_shared_tasks():
    user_id = get_jwt_identity()
    shared_tasks = TaskShare.query.filter_by(user_id=user_id).all()
    return jsonify([task.task.to_dict() for task in shared_tasks]), 200

@bp.route('/tasks/<int:task_id>/share', methods=['POST'])
@jwt_required()
def share_task(task_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    share = TaskShare(
        task_id=task_id,
        user_id=data['user_id'],
        permission=data.get('permission', 'view')
    )
    
    db.session.add(share)
    db.session.commit()
    
    return jsonify({'message': 'Task shared successfully'}), 200

@bp.route('/tasks/<int:task_id>/attachment', methods=['POST'])
@jwt_required()
def add_attachment(task_id):
    user_id = get_jwt_identity()
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    filename = secure_filename(file.filename)
    file_path = os.path.join('uploads', filename)
    
    # Ensure uploads directory exists
    os.makedirs('uploads', exist_ok=True)
    
    file.save(file_path)
    
    attachment = Attachment(
        filename=filename,
        file_path=file_path,
        task_id=task_id
    )
    
    db.session.add(attachment)
    db.session.commit()
    
    return jsonify({
        'id': attachment.id,
        'filename': attachment.filename
    }), 201

@bp.route('/tasks/stats', methods=['GET'])
@jwt_required()
def get_task_stats():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    stats = user.get_task_stats()
    
    # Add category-wise stats
    category_stats = []
    for category in user.categories:
        category_stats.append({
            'category': category.name,
            'total_tasks': category.tasks.count(),
            'completed_tasks': category.tasks.filter_by(completed=True).count()
        })
    
    stats['category_stats'] = category_stats
    return jsonify(stats), 200 