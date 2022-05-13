from sqlalchemy import ForeignKey
from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_json(self):
        task_dict = {"id": self.task_id,
                    "title": self.title,
                    "description": self.description,
                    "is_complete": bool(self.completed_at)}
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id
        return task_dict

    @classmethod
    def from_json(cls, json):
        task = Task(title = json["title"],
                    description = json["description"],
                    completed_at = json.get("completed_at"),
                    goal_id = json.get("goal_id"))
        return task