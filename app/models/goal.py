from app import db
from flask import abort, make_response

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column("title", db.String , nullable = False)
    tasks = db.relationship("Task", back_populates = "goal", lazy = True)

    def to_json(self):
        return {
            "id":self.goal_id,
            "title":self.title
        }

    @classmethod
    def create(cls, request_body):
        try:
            new_goal = cls(title=request_body["title"])
        except KeyError:
            return abort(make_response({"details": "Invalid data"}, 400))

        return new_goal



