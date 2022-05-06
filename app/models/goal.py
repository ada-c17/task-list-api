from app import db
from flask import abort, make_response


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)


    def to_json(self):
        return {
            "id" : self.id,
            "title" : self.title
            }

    @classmethod
    def create_task(cls, request_body):
        try:
            new_task = cls(title=request_body['title'])
            return new_task
        except:
            return abort(make_response({"details": "Invalid data"}, 400))