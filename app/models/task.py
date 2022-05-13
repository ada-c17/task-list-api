from app import db
from flask import make_response, abort


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable= True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable = True)
    goal= db.relationship("Goal", back_populates="tasks")

#Helper funtion for validation of input, this only works for Task.
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({'details': 'Invalid task id'}, 400))
    tasks = Task.query.all()
    for task in tasks:
        if task_id == task.task_id:
            return task
    abort(make_response ({'details': 'This task does not exist'}, 404))