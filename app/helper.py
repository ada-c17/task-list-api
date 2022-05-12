from flask import Blueprint, jsonify, request, make_response, abort
from app.models.task import Task
from app.models.goal import Goal


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"task {task_id} not found"}, 404))

    return task

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message": f"goal {goal_id} not found"}, 404))

    return goal
