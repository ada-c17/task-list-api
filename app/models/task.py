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
    
    def to_json(task):
        return {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete()
        }

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
    def from_json(cls):
        pass 
