from flask import abort, make_response
from app.models.task import Task
import requests

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