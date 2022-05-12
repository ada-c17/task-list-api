from email.policy import default
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String) #check for nullable=False
    completed_at = db.Column(db.DateTime, default=None)

    def to_json(self):

        if not self.completed_at:
            completed_at = False

        return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": completed_at
            }