from flask import abort, make_response
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_json(self): 
        response_body = {
            "id": self.goal_id,
            "title": self.title
        }
        return response_body

# Class method to create a new goal 
    @classmethod
    def create(cls, request_body):
        if "title" not in request_body:
            abort(make_response({"details": "Invalid data"}, 400))
        new_goal = cls(
            title=request_body["title"]
        )
        return new_goal

# Method to update goals
    def update(self, request_body):
        self.title = request_body["title"]