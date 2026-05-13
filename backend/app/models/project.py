from app.database.base_repository import BaseRepository
from bson import ObjectId

class ProjectRepository(BaseRepository):
    def __init__(self):
        super().__init__("projects")

    def find_by_user(self, user_id, **kwargs):
        filters = kwargs.get('filters', {})
        filters['user_id'] = user_id
        return self.list(filters=filters, **kwargs)

    def duplicate(self, project_id, new_name=None):
        project = self.get_by_id(project_id)
        if not project:
            return None
        
        # Prepare new project data
        new_project = project.copy()
        new_project.pop('_id')
        new_project['project_name'] = new_name or f"{project['project_name']} (Copy)"
        new_project['created_at'] = None # BaseRepository will set this
        new_project['updated_at'] = None
        
        return self.create(new_project)

project_repo = ProjectRepository()
