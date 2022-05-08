from app import db
from sqlalchemy.orm import relationship
from .task import Task
from .common import define_validation_on_model


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
    
    @classmethod
    @define_validation_on_model
    def validate_id(cls, target_id):
        pass
