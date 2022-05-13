from app import db
from app.error_responses import MissingValueError

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship('Task', back_populates='goal')

    @classmethod
    def create(cls, goal_details):
        if 'title' not in goal_details:
            raise MissingValueError
        return cls(title = goal_details['title'])
    
    def update(self, new_details):
        for k,v in new_details.items():
            if k in self.__dict__:
                setattr(self, k, v)


class TasksGoal():
    def __init__(self, goal):
        self._ = goal
