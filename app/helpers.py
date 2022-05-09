from flask import abort, make_response
from app.models.task import Task
from app.models.goal import Goal
import requests
import os

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

def display_goal(goal):
    return {
        "id": goal.goal_id,
        "title": goal.title
    }

def valid_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"msg":f"Task id {goal_id} invalid"}, 400))
    
    goal = Goal.query.get(goal_id)
    if not goal:
        abort(make_response({"msg":f"Task id {goal_id} not found"}, 404))

    return goal