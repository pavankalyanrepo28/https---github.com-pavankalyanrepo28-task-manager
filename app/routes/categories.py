from flask import Blueprint, request, jsonify
from app.models import Category
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('categories', __name__)

@bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    user_id = get_jwt_identity()
    categories = Category.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': cat.id,
        'name': cat.name,
        'color': cat.color,
        'task_count': cat.tasks.count()
    } for cat in categories]), 200

@bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    category = Category(
        name=data['name'],
        color=data.get('color', '#000000'),
        user_id=user_id
    )
    
    db.session.add(category)
    db.session.commit()
    
    return jsonify({
        'id': category.id,
        'name': category.name,
        'color': category.color
    }), 201 