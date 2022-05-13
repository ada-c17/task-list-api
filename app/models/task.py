from cgitb import handler
from sqlalchemy import null
from app import db
from app.handler import Handler
from flask import request


class Task(db.Model, Handler):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.id"), nullable=True)

    def to_dict(self):
        if self.goal_id:
            return dict(
                id = self.id,
                goal_id = self.goal_id,
                title = self.title,
                description=self.description,
                is_complete = bool(self.completed_at)
            )
        return dict(
            id = self.id,
            title = self.title,
            description=self.description,
            is_complete = bool(self.completed_at)
        )

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
                title=data_dict["title"],
                description=data_dict["description"],
                completed_at = data_dict.get("completed_at", None)
            )