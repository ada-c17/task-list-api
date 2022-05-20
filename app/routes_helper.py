from flask import make_response, abort
from app.models.task import Task
from app.models.goal import Goal


def get_task_by_id(task_id):
    try:
        task_id = int(task_id)
    except:
        abort_message("Invalid data", 400)

    task = Task.query.get(task_id)

    if not task:
        abort_message("Task not found", 404)
    return task


def get_goal_by_id(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort_message("Invalid data", 400)

    goal = Goal.query.get(goal_id)

    if not goal:
        abort_message("Goal not found", 404)
    return goal


def get_record_by_id(cls, record_id):
    try:
        record_id = int(record_id)
    except:
        abort_message("Invalid data", 400)

    record = cls.query.get(record_id)

    if not record:
        abort_message(f"{type(cls).__name__} not found", 404)
    return record


def abort_message(details_info, status_code=200):
    abort(make_response({"details": details_info}, status_code))