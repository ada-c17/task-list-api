from app import db
from flask import jsonify, abort, make_response

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)

    def to_json(self):
        is_complete = self.completed_at != None
        return {
            "id" : self.id,
            "title" : self.title,
            "description" : self.description,
            "is_complete" : is_complete
            }

    @classmethod
    def create_task(cls, request_body):
        try: 
            new_task = cls(
                title=request_body['title'],
                description=request_body['description']
            )
            return new_task
        except:
            return abort(make_response({"details": "Invalid data"}, 400))