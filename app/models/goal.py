from app import db
from app.routes.utils.helper import get_JSON_request_body
from flask import request, abort, make_response


class Goal(db.Model):

    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, unique=True, nullable=False)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_JSON_response(self):
        return {
            "goal": {
                "id": self.goal_id,
                "title": self.title
            }
        }

    @staticmethod
    def from_JSON_request():
        payload = get_JSON_request_body(request)

        if "title" not in payload:
            abort(make_response({"details": "Invalid data"}, 400))

        return Goal(title=payload["title"])

    def update_from_JSON_request(self):
        payload = get_JSON_request_body(request)

        if "title" not in payload:
            abort(make_response({"details": "Invalid data"}, 400))

        self.title = payload["title"]
