from app import db
from flask import abort, make_response, jsonify
from sqlalchemy.orm import relationship
from .task import Task


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = relationship(Task)

    def to_json(self, include_tasks=False):
        if not include_tasks:
            return {
                'id': self.goal_id,
                'title': self.title
            }
        return {
            'id': self.goal_id,
            'title': self.title,
            'tasks': [task.to_json() for task in self.tasks]
        }
    
    # TODO: refactor validate_id as a decorator
    @classmethod
    def validate_id(cls, target_id):
        try:
            target_id = int(target_id)
        except:
            abort(make_response(jsonify(f"{target_id} is not a valid id."),400))
        
        goal = cls.query.get(target_id)

        if not goal:
            abort(make_response(jsonify(f"A goal with id of {target_id} was not found."),404))
        
        return goal
