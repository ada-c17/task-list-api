from app.models.task import Task
from app.models.goal import Goal
from flask import abort, make_response,request

def validate_task(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"Task{id} is invalid"}, 400))

    task = Task.query.get(id)
    if not task:
        abort(make_response({"message": f"Task{id} not found"}, 404))

    return task


def validate_client_requests(request_body):
    try:
        new_task = Task.create(request_body)
    except KeyError:
        abort(make_response({"details": "Invalid data"},400))
    
    return new_task
    
    
def validate_goal(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"Goal{id} is invalid"}, 400))

    goal = Goal.query.get(id)
    if not goal:
        abort(make_response({"message": f"Goal{id} not found"}, 404))

    return goal

def goal_validate_client_requests(request_body):
    try:
        new_goal = Goal.create(request_body)
    except KeyError:
        abort(make_response({"details": "Invalid data"},400))
    
    return new_goal
