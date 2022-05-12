from app import db
from datetime import datetime 

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def task_to_json(self):
        response = { 
            "id": self.id, 
            "title": self.title,
            "description": self.description,
            "is_complete": isinstance(self.completed_at, datetime)
        }

        if self.goal_id:
            response["goal_id"] = self.goal_id
        return response 


