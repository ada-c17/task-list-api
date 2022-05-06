from sqlalchemy import null
from app import db
from flask import make_response, abort

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)

    title = db.Column("title",db.String)

    description = db.Column("description", db.String)

    completed_at = db.Column("completed_at", db.DateTime, default=None)




    def to_json(self):
        if self.completed_at == None:
            return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": False
            }
        else:
            return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": True
            }

    @classmethod
    def create(cls, request_body):
        try:
            new_task = cls(title=request_body["title"], description=request_body["description"],completed_at = None
            )
        except KeyError:
            return abort(make_response({"details": "Invalid data"}, 400))

        return new_task

    def update(self, request_body):
        self.title = request_body["title"]
        self.description = request_body["description"]
        self.completed_at = None
