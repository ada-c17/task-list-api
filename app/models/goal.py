from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship('Task', back_populates='goal')


class TasksGoal():
    def __init__(self, goal):
        self.goal = goal
