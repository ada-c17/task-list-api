from flask import Blueprint, request, jsonify, abort, make_response
from app import db
from app.models.goal import Goal
from app.models.task import Task

def get_task_or_abort(task_id):
    """
    Checking the id task from input:
        - return object task if id is integer
        - raise exception if id is not integer then return status code 400,
        but if the id not exist then return status code 404

    """
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({"message": f"The task id {task_id} is invalid. The id must be integer."}, 400))
    
    tasks = Task.query.all()
    for task in tasks:
        if task.id == task_id:
            return task
    abort(make_response({"message": f"The task id {task_id} is not found"}, 404))


# helper function to check title or description of key dictionary exist or not
def validate_input_key_for_post_or_update():
    """Checking missing data key when post or update
        - raise exception if the key doesn't exist
        - return request object if the key exist
    """
    request_task = request.get_json()
    if "title" not in request_task or "description" not in request_task:
        abort(make_response({"details": "Invalid data"}, 400))
    return request_task


# helper function to check goal id
def get_goal_or_abort(goal_id):
    """
    Checking the id goal from input:
        - return object goal if id is integer
        - raise exception if id is not integer then return status code 400,
        but if the id not exist then return status code 404

    """
    try:
        goal_id = int(goal_id)
    except ValueError:
        abort(make_response({"message": f"The goal id {goal_id} is invalid. The id must be integer."}, 400))
    
    goals = Goal.query.all()
    for goal in goals:
        if goal.id == goal_id:
            return goal
    abort(make_response({"message": f"The goal id {goal_id} is not found"}, 404))


# helper function to check title key dictionary exist or not
def validate_title_key_for_post_or_update():
    """Checking missing title key when post or update
        - raise exception if the key doesn't exist
        - return request object if the key exist
    """
    request_goal = request.get_json()
    if "title" not in request_goal:
        abort(make_response({"details": "Invalid data"}, 400))
    return request_goal
