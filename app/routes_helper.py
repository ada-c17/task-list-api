from flask import make_response, abort
from app.models.task import Task
from app.models.goal import Goal

# maybe the ids can reactored into 1 function?
def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except:
        create_message("Invalid data", 400)

    task = Task.query.get(task_id)

    if not task:
        create_message("Task not found", 404)
    return task


def validate_goal_id(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        create_message("Invalid data", 400)

    goal = Goal.query.get(goal_id)

    if not goal:
        create_message("Goal not found", 404)
    return goal


def create_message(details_info, status_code=200):
    abort(make_response({"details": details_info}, status_code))