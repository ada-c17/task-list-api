from app import db
from flask import current_app


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))
    goal = db.relationship("Goal", back_populates = "tasks")


    def make_json(self):
            if not self.completed_at:
                is_complete = False
            else:
                is_complete = True
            
            return {
                "id": self.task_id,
                # "goal_id": self.goal_id,
                "title": self.title,
                "description": self.description,
                "is_complete": is_complete
            }