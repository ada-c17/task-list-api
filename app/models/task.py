from datetime import datetime
from sqlalchemy import null
from app import db
from flask import make_response, abort

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column("title",db.String)
    description = db.Column("description", db.String)
    completed_at = db.Column("completed_at", db.DateTime, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="tasks")




    def to_json(self):

        is_complete = True if self.completed_at else False

        response_body = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }

        if self.goal_id: response_body["goal_id"] = self.goal_id 
        
        return response_body


    @classmethod
    def create(cls, request_body):
        try:
            new_task = cls(title=request_body["title"], description=request_body["description"], completed_at=request_body.get("completed_at"), goal_id=request_body.get("goal_id")
            )
        except KeyError:
            return abort(make_response({"details": "Invalid data"}, 400))

        return new_task

    def update(self, request_body):
        self.title = request_body["title"]
        self.description = request_body["description"]
        self.completed_at = request_body.get("completed_at")
    
    def mark_complete(self):
        self.completed_at = datetime.now()

    def mark_incomplete(self):
        self.completed_at = None
