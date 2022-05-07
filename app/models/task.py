from app import db
from flask import abort, make_response, jsonify


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)

    def to_json(self):
        return {
            'id': self.task_id,
            'title': self.title,
            'description': self.description,
            'is_complete': self.completed_at != None,
            'goal_id': self.goal_id
        }
    
    @classmethod
    def validate_id(cls, target_id):
        try:
            target_id = int(target_id)
        except:
            abort(make_response(jsonify(f"{target_id} is not a valid id."),400))
        
        task = cls.query.get(target_id)

        if not task:
            abort(make_response(jsonify(f"A task with id of {target_id} was not found."),404))
        
        return task
