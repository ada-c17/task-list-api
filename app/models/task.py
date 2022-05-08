from app import db
from .common import define_validation_on_model


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)

    def to_json(self):
        details = {
                'id': self.task_id,
                'title': self.title,
                'description': self.description,
                'is_complete': self.completed_at != None
            }
        if self.goal_id:
            details['goal_id'] = self.goal_id
        return details
    
    @classmethod
    @define_validation_on_model
    def validate_id(cls, target_id):
        pass
