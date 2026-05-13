from app.database.base_repository import BaseRepository

class ScriptRepository(BaseRepository):
    def __init__(self):
        super().__init__("scripts")

    def find_by_project(self, project_id):
        return self.list(filters={"project_id": project_id}, limit=100)

script_repo = ScriptRepository()
