from sqlalchemy import ForeignKey
from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="tasks")

    def todict(self):
        return {"id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": bool(self.completed_at)}