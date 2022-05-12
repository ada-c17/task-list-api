from app.models.task import Task
from app.models.goal import Goal
from flask import jsonify, make_response, abort

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response(jsonify(dict(details=f"Invalid task id: {task_id}")), 400))
    
    task = Task.query.get(task_id)

    if not task:
        abort(make_response(jsonify(dict(details=f"Task not found")), 404))
    else:
        return task

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response(jsonify(dict(details=f"Invalid goal id: {goal_id}")), 400))
    
    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response(jsonify(dict(details=f"Goal not found")), 404))
    else:
        return goal