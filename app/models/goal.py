from app import db
from flask import make_response, abort


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)


# Helper funtion for validation of input, this only works for Goal.
def validate_goal(goal_id):
    goal_id = int(goal_id)
    goals = Goal.query.all()
    for goal in goals:
        if goal_id == goal.goal_id:
            return goal
    abort(make_response ({'details': 'This goal does not exist'}, 404))
