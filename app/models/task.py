from app import db
from flask import make_response, abort

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def is_complete(self):
        if not self.completed_at:
            return False 
        else:
            return True 
    
    def to_json(self):
        json = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete()
        }

        if self.goal_id:
            json["goal_id"] = self.goal_id

        return json 

    def validate_task(task_id):
        try:
            task_id = int(task_id)
        except ValueError:
            abort(make_response({"message":f"Task {task_id} invalid"}, 400))

        
        task = Task.query.get(task_id)
        if not task:
            abort(make_response({"message":f"Task {task_id} not found"}, 404))
        
        return task 

    @classmethod
    def from_json(cls, task_json):
        title = task_json["title"]
        description = task_json["description"]
        completed_at = task_json["completed_at"]

        task = cls(title, description, completed_at)

        return task