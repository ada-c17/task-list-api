from app import db
from flask import make_response, abort


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)

    def to_json(self,task=True):
        response = {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": bool(self.completed_at)
                }
        if task:
            response = { 
                "task": response}
        return response

    @classmethod
    def from_json(cls,json_obj):
        return Task(title=json_obj["title"],
                    description=json_obj["description"],
                    completed_at=json_obj["completed_at"])
    
    @classmethod
    def validate_id(cls,id):
        try:
            id = int(id)
        except ValueError:
            abort(make_response({"details":"Invalid data"}, 400))
        task = cls.query.get(id)
        if not task:
            abort(make_response({"details":f"Task #{id} does not exist"}, 404))
        return task