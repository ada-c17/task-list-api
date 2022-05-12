from app import db
from app.routes.utils.helper import get_JSON_request_body
from flask import abort, make_response, request


class Task(db.Model):

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks", lazy=True)

    def to_JSON_response(self):
        payload = {
            "task": {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": bool(self.completed_at)
            }
        }

        if self.goal_id:
            payload["task"]["goal_id"] = self.goal_id

        return payload

    @staticmethod
    def from_JSON_request():
        payload = get_JSON_request_body(request)

        if "title" not in payload or "description" not in payload:
            abort(make_response({"details": "Invalid data"}, 400))

        return Task(title=payload["title"],
                    description=payload["description"],
                    completed_at=payload.get("completed_at", None),
                    goal_id=payload.get("goal_id", None))

    def update_from_JSON_request(self):
        payload = get_JSON_request_body(request)

        if "title" in payload:
            self.title = payload["title"]
        
        if "description" in payload:
            self.description = payload["description"]

        if "completed_at" in payload:
            self.completed_at = payload["completed_at"]

        if "goal_id" in payload:
            self.goal_id = payload["goal_id"]
