from app import db
from flask import make_response
from sqlalchemy import asc
from datetime import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True, default = None)


    def to_json(self):
        json_response = {
            "id": self.task_id,
            "title": self.title,
            "description":self.description,
        }
        if self.completed_at:
            json_response["is_complete"] = True
        else:
            json_response["is_complete"] = False
        return json_response

    def update_task(self, request_body):
        self.title = request_body["title"]
        self.description = request_body["description"]
        
        

    @classmethod
    def create_task(cls, request_body):
        # data_valid= validate_data(request_body)
        new_task = cls(title = request_body["title"],
                        description = request_body["description"]
            )
        
        return new_task
