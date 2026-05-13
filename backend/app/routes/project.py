from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError

from app.services.project_service import ProjectService
from app.validators.project_validator import ProjectCreateSchema, ProjectUpdateSchema

project_bp = Blueprint('projects', __name__)

@project_bp.route('/create', methods=['POST'])
@jwt_required()
def create_project():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400
        
        project_data = ProjectCreateSchema(**data)
        project = ProjectService.create_project(user_id, project_data.dict())
        
        return jsonify(project), 201
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@project_bp.route('', methods=['GET'])
@jwt_required()
def get_projects():
    user_id = get_jwt_identity()
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    search = request.args.get('search')
    folder = request.args.get('folder')
    
    projects = ProjectService.get_user_projects(user_id, page, limit, search, folder)
    return jsonify(projects), 200

@project_bp.route('/<project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    user_id = get_jwt_identity()
    project = ProjectService.get_project_details(user_id, project_id)
    
    if not project:
        return jsonify({"error": "Project not found"}), 404
        
    return jsonify(project), 200

@project_bp.route('/<project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        update_data = ProjectUpdateSchema(**data)
        project = ProjectService.update_project(user_id, project_id, update_data.dict(exclude_unset=True))
        
        if not project:
            return jsonify({"error": "Project not found or unauthorized"}), 404
            
        return jsonify(project), 200
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@project_bp.route('/<project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    user_id = get_jwt_identity()
    success = ProjectService.delete_project(user_id, project_id)
    
    if not success:
        return jsonify({"error": "Project not found or unauthorized"}), 404
        
    return jsonify({"message": "Project deleted successfully"}), 200

@project_bp.route('/duplicate', methods=['POST'])
@jwt_required()
def duplicate_project():
    user_id = get_jwt_identity()
    data = request.get_json()
    project_id = data.get('project_id')
    
    if not project_id:
        return jsonify({"error": "project_id is required"}), 400
        
    new_project = ProjectService.duplicate_project(user_id, project_id)
    
    if not new_project:
        return jsonify({"error": "Project not found or unauthorized"}), 404
        
    return jsonify(new_project), 201
