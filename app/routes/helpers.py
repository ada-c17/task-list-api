from flask import abort, make_response
from app.models.task import Task
from app.models.goal import Goal
import requests
import os
from datetime import datetime

def post_slack_message(text):
    URL = "https://slack.com/api/chat.postMessage"
    token = os.environ.get("SLACK_TOKEN")
    params = {
        "channel":"task-notifications",
        "text":text
    }
    headers = {
        "Authorization" : "Bearer " + token
    }

    response = requests.post(URL, headers=headers, params=params)
    response_body = response.json()
    return response_body["ok"]

def valid_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"msg":f"Task id {task_id} invalid"}, 400))

    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"msg":f"Task id {task_id} not found"}, 404))

    return task

def display_task(task):
    return {
        "id" : task.task_id,
        "title" : task.title,
        "description" : task.description,
        "is_complete" : False if not task.completed_at else True
    }

def display_goal(goal):
    return {
        "id": goal.goal_id,
        "title": goal.title
    }

def valid_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"msg":f"Goal id {goal_id} invalid"}, 400))
    
    goal = Goal.query.get(goal_id)
    if not goal:
        abort(make_response({"msg":f"Goal id {goal_id} not found"}, 404))

    return goal

def check_completed_at(request_body):
    if "completed_at" not in request_body:
        return None
    time = request_body["completed_at"]
    try:
        # utcnow() data string format: 'Thu, 12 May 2022 04:19:18 GMT'
        return datetime.strptime(time, '%a, %d %b %Y %H:%M:%S GMT')
    except ValueError:
        abort(make_response({"msg":f"Complete_at Time {time} invalid"}, 400))