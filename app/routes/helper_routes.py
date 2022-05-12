from flask import request, make_response, abort, jsonify
# import requests
from app.models.task import Task
from app.models.goal import Goal
# from app import db
# from datetime import date
# import os
import requests


def validate_id(id):
    if "/goals" in request.path or "/goals/<goal_id>" in request.path:
        try:
            goal_id = int(id)
        except ValueError:
            abort(make_response(jsonify(f"Goal {goal_id} is invalid"), 400))
        goal = Goal.query.get(goal_id)
        if not goal:
            abort(make_response(jsonify(f"Goal {goal_id} not found"), 404))
        return goal
    if "/tasks" in request.path:
        try:
            task_id = int(id)
        except ValueError:
            abort(make_response(jsonify(f"Task {task_id} is invalid"), 400))
        task = Task.query.get(task_id)
        if not task:
            abort(make_response(jsonify(f"Task {task_id} not found"), 404))
        return task

# VALIDATE REQUEST
def validate_request(request):
    request_body = request.get_json()
    
    if "/goals" in request.path and "/tasks" in request.path:
        try:
            request_body["task_ids"]
        except KeyError:
            abort(make_response({"details": "Invalid data"}, 400)) 
        return request_body
    elif "/goals" in request.path:
        try:
            request_body["title"]
        except KeyError:
            abort(make_response({"details": "Invalid data"}, 400)) 
        return request_body
    try:
        request_body["title"]
        request_body["description"]
    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400)) 
    return request_body

