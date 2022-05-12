from sqlalchemy import ForeignKey
from app import db
from flask import abort, make_response, request


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_json(self):

        response_body = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at)
        }

        if self.goal_id:
            response_body["goal_id"] = self.goal_id

        return response_body
    
    @staticmethod
    def from_json():
        request_body = request.get_json()

        if "title" not in request_body or "description" not in request_body:
            abort(make_response({"details": "Invalid data"}, 400))

        return Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body.get("completed_at", None),
                    goal_id=request_body.get("goal_id", None))