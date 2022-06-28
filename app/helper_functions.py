from flask import abort, make_response,jsonify
from app.models.task import Task
from app.models.goal import Goal

def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

#------------------TASK RELATED HELPER FUNCTIONS------------------------
def update_task_safely(task, data_dict):
    try:
        task.update_self(data_dict)
    except ValueError as err:
        error_message(f"Invalid key(s): {err}. Task not updated.", 400)

        
def get_task_record_by_id(id):
    try:
        id = int(id)
    except ValueError:
        abort(make_response(jsonify(dict(details=f"Invalid id: {id}")),400))
    task = Task.query.get(id)
    if task:
        return task
    else:
        abort(make_response(jsonify(dict(details=f"Invalid id: {id}")),404))

#------------------GOAL RELATED HELPER FUNCTIONS------------------------
def update_goal_safely(goal, data_dict):
    try:
        goal.update_self(data_dict)
    except ValueError as err:
        error_message(f"Invalid key(s): {err}. Task not updated.", 400)
        
def get_goal_record_by_id(id):
    try:
        id = int(id)
    except ValueError:
        abort(make_response(jsonify(dict(details=f"Invalid id: {id}")),400))
    goal = Goal.query.get(id)
    if goal:
        return goal
    else:
        abort(make_response(jsonify(dict(details=f"Invalid id: {id}")),404))