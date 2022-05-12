from app import db
from flask import abort, make_response, request

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', back_populates='goal', lazy=True)

    def to_json(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }
    
    @staticmethod
    def from_json():
        request_body = request.get_json()
        if "title" not in request_body:
            abort(make_response({"details": "Invalid data"}, 400))
        return Goal(title=request_body["title"])
        