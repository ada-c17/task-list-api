from app import db
from app.commons import MissingValueError

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship('Task', back_populates='goal')

    @classmethod
    def create(cls, goal_details):
        if 'title' not in goal_details:
            raise MissingValueError
        return cls(title = goal_details['title'])


class TasksGoal():
    def __init__(self, goal):
        self._ = goal
