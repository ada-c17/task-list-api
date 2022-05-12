from requests import request
from app import db
from flask import abort, make_response

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True)
    goals = db.relationship("Goal")

    def to_json(self):
        is_complete = self.completed_at != None
        # try:
        hash_map = {
            "id" : self.id,
            "title" : self.title,
            "description" : self.description,
            "is_complete" : is_complete
            }
        if self.goal_id:
            hash_map["goal_id"] = self.goal_id

        return hash_map
    

    @classmethod
    def create_task(cls, request_body):
        try:
            try:
                new_task = cls(
                title=request_body['title'],
                description=request_body['description'],
                completed_at=request_body['completed_at'])
            except KeyError: 
                new_task = cls(
                title=request_body['title'],
                description=request_body['description'],)

            return new_task
        except:
            return abort(make_response({"details": "Invalid data"}, 400))