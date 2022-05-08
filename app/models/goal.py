from app import db
from flask import make_response, abort 

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)

    def to_json(self):
        
        return {"id" : self.goal_id,
                "title" : self.title}
    

    def update_goal(self, update_body):
            self.title = update_body["title"]


    @classmethod
    def from_json(cls, request_body):

        if "title" not in request_body:
            abort(make_response({"details": "Invalid data"}, 400))

        new_goal = cls(
            title=request_body["title"])

        return new_goal


