from app import db
from flask import make_response, abort


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    def to_json(self,goal=True):
        response = {
                "id": self.goal_id,
                "title": self.title,
                }
        if goal:
            response = { 
                "goal": response}
        return response

    @classmethod
    def from_json(cls,request_body):
        try:
            return cls(title=request_body["title"])
        except KeyError:
            return abort(make_response({"details":"Invalid data"},400))
    
    @classmethod
    def validate_id(cls,id):
        try:
            id = int(id)
        except ValueError:
            abort(make_response({"details":"Invalid data"}, 400))
        goal = cls.query.get(id)
        if not goal:
            abort(make_response({"details":f"Goal #{id} does not exist"}, 404))
        return goal