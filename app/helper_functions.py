from flask import abort, make_response
from app.models.task import Task
from app.models.goal import Goal


def validate_task_or_abort(task_id):
    # returns 400 error if invalid task_id (alpha/non-int) 
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({"error": f"{task_id} is an invalid task id"}, 400))
    
    # returns 404 error if task_id not found in database
    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"error": f"Task {task_id} not found"}, 404))
    return task


def validate_goal_or_abort(goal_id):
    # returns 400 error if invalid goal_id (alpha/non-int) 
    try:
        goal_id = int(goal_id)
    except ValueError:
        abort(make_response({"error": f"{goal_id} is an invalid goal id"}, 400))
    
    # returns 404 error if goal_id not found in database
    goal = Goal.query.get(goal_id)
    if not goal:
        abort(make_response({"error": f"Goal {goal_id} not found"}, 404))
    return goal