from app import db
from flask import make_response
from sqlalchemy import asc
from datetime import datetime
# from app.models.goal import Goal


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True, default = None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("goal", back_populates="tasks")

    def to_json(self):
        json_response = {
            "id": self.task_id,
            "title": self.title,
            "description":self.description
        }
        if self.completed_at:
            json_response["is_complete"] = True
        else:
            json_response["is_complete"] = False

        if self.goal_id:
            json_response["goal_id"] =self.goal_id

        return json_response

    def update_task(self, request_body):
        self.title = request_body["title"]
        self.description = request_body["description"]
        if self.completed_at:
            if self.completed_at == request_body['completed_at']:
                self.completed_at = datetime.utcnow()
        


    @classmethod
    def create_task(cls, request_body):

        new_task = cls(title = request_body["title"],
                    description = request_body["description"],
                    completed_at = request_body.get("completed_at", None)
            )
        
        return new_task
