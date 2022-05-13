from sqlalchemy import ForeignKey
from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None)  
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable = True)


    def to_dict(self):
        if self.goal_id:
            return {
                "id": self.id,
                "goal_id": self.goal_id,
                "title": self.title,
                "description": self.description,
                "is_complete": bool(self.completed_at)
            }
        else:
            return {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": bool(self.completed_at),
            }