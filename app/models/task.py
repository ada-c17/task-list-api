from app import db
from flask import jsonify, abort, make_response

class Task(db.Model):

    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completred_at = db.Column(db.Datetime, nullable = True)

    def to_json(self):
        if not self.completed_at:
            is_complete = False
        else:
            is_complete = True

        return {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.is_complete
        }
