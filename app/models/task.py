from app import db
from flask import Blueprint, jsonify


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)


    # def format_response_body(self):
    #     if not self.completed_at:
    #         completed_task = False
    #     else:
    #         completed_task = True 
        
    #     task_response_body = {
    #         "id": self.task_id,
    #         "title": self.title,
    #         "description": self.description,
    #         "is_complete": completed_task
    #     }

    #     return task_response_body