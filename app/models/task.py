from app import db
from flask import make_response, abort


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable= True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable = True)
    goal= db.relationship("Goal", back_populates="tasks")


# Helper funtion for validation of input, this only works for Task.
def validate_task(task_id):
    task_id = int(task_id)
    tasks = Task.query.all()
    for task in tasks:
        if task_id == task.task_id:
            return task
    abort(make_response ({'details': 'This task does not exist'}, 404))


# Creates the response for routes where task are selected from the existing ones.
def format_response_existing(chosen_task):
    response_body= {'task': {  
            'id' :chosen_task.task_id,
            'title': chosen_task.title,
            'description': chosen_task.description,
            'is_complete': is_completed(chosen_task.completed_at)}}

    return response_body


# Creates the response for routes where task is new.
def format_response_new(new_task):
    response_body= {'task': {  
            'id' : new_task.task_id,
            'title': new_task.title,
            'description': new_task.description,
            'is_complete': is_completed(new_task.completed_at)}}
    return response_body


# Function to verify is task is comleted or not
def is_completed(completed_at):
    if completed_at is None:
        return False
    else: 
        return True