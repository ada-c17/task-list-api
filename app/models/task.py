from app import db
from flask import Blueprint, jsonify, make_response, request, abort



class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.Unicode)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_key = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    # goal = db.relationship("Goal", back_populates="tasks")
    
    

    
    def to_dict(self):
        return (dict(task={
            "id" : self.task_id,
            "title": self.title,
            "description" : self.description,
            "is_complete" : bool(self.completed_at)
        }))
    
    def dict_rel(self):
        return (dict(task={
            "id" : self.task_id,
            "title": self.title,
            "description" : self.description,
            "is_complete" : bool(self.completed_at),
            "goal_id" : self.goal_key
        }))

