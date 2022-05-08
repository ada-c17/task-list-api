from flask import abort, make_response
from app.models.task import Task
import requests
import os 

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)    
    if not task: 
        return abort(make_response({"message":f"task {task_id} not found"}, 404))
        
    return task

def send_slack_completed_message(task):

    PATH = "https://slack.com/api/chat.postMessage"

    API_KEY = os.environ.get(
            "SLACK_API_KEY")
    BEARER_TOKEN = os.environ.get(
            "AUTH_TOKEN_SLACK")

    query_params = {"channel" : "task-notifications", "text": f'Someone just completed the task {task.title}' }
    headers = {"authorization" : BEARER_TOKEN}
    # data = {"data": "f'Someone just completed the task {task.title}"}

    response_body = requests.get(PATH, params=query_params, headers=headers)