from app.models.project import project_repo
from app.models.script import script_repo
from app.utils.logger import request_logger

class ProjectService:
    @staticmethod
    def create_project(user_id, project_data):
        project_data['user_id'] = user_id
        project_data['archived'] = False
        project = project_repo.create(project_data)
        request_logger.info(f"Project created: {project['_id']} by user {user_id}")
        return project

    @staticmethod
    def get_user_projects(user_id, page=1, limit=10, search=None, folder=None):
        filters = {"user_id": user_id, "archived": False}
        
        if search:
            filters["project_name"] = {"$regex": search, "$options": "i"}
        
        if folder:
            filters["folder_name"] = folder
            
        return project_repo.list(filters=filters, page=page, limit=limit)

    @staticmethod
    def get_project_details(user_id, project_id):
        project = project_repo.get_by_id(project_id)
        if not project or project['user_id'] != user_id:
            return None
        
        # Optionally include scripts
        scripts = script_repo.find_by_project(project_id)
        project['scripts'] = scripts['items']
        
        return project

    @staticmethod
    def update_project(user_id, project_id, update_data):
        project = project_repo.get_by_id(project_id)
        if not project or project['user_id'] != user_id:
            return None
        
        return project_repo.update(project_id, update_data)

    @staticmethod
    def delete_project(user_id, project_id):
        project = project_repo.get_by_id(project_id)
        if not project or project['user_id'] != user_id:
            return False
        
        # Soft delete by archiving or hard delete?
        # User requested DELETE endpoint, let's do hard delete for now but could be soft.
        return project_repo.delete(project_id)

    @staticmethod
    def duplicate_project(user_id, project_id):
        project = project_repo.get_by_id(project_id)
        if not project or project['user_id'] != user_id:
            return None
        
        new_project = project_repo.duplicate(project_id)
        
        # Duplicate scripts as well
        scripts = script_repo.find_by_project(project_id)
        for script in scripts['items']:
            new_script = script.copy()
            new_script.pop('_id')
            new_script['project_id'] = new_project['_id']
            script_repo.create(new_script)
            
        request_logger.info(f"Project duplicated: {project_id} -> {new_project['_id']}")
        return new_project
