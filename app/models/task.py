from app import db
from flask_json import json

from flask import current_app, abort, make_response, json_encoder


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))
    goal = db.relationship("Goal", back_populates = "tasks")

    @json.encoder
    def make_json(self):
        if not self.completed_at:
            is_complete = False
        else:
            is_complete = True
        dic_table = {}
        if not self.goal_id: 
            dic_table["id"] = self.task_id
            dic_table["title"] = self.description
            dic_table["is_complete"] = is_complete
            return dic_table
        else:
            dic_table["id"] = self.task_id
            dic_table["goal_id"] = self.goal_id
            return dic_table

    @classmethod
    def valid_task(cls, request_body):
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
 
