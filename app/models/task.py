from app import db
from datetime import datetime


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))
    goal = db.relationship("Goal", back_populates="tasks")

    def to_json(self):
        complete = True if self.completed_at else False

        if self.goal_id:
            return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": complete,
            "goal_id": self.goal_id
            }
        else:
            return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": complete
            }   