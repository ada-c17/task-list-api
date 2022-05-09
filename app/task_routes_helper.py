from flask import abort, make_response, jsonify
from app.models.task import Task
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def check_task_exists(task_id):
    task = Task.query.get(task_id)

    if not task:
        abort(make_response(jsonify({"error": f"Task {task_id} does not exist"}), 404))
    
    return task

def try_to_make_task(response_body):
    try:
        return Task.make_task(response_body)
    except KeyError:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))

def post_task_to_slack(task):
    path = "https://slack.com/api/chat.postMessage"
    slack_message = f"Someone just completed the task {task.title}"

    query_params = {"token": os.environ.get("SLACKBOT_TOKEN"), 
                    "channel": "task-notifications", 
                    "text": slack_message}

    response = requests.post(path, data=query_params)

