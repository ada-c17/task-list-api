from flask import jsonify, make_response, abort
from app.models.goal import Goal
from app.models.task import Task
import requests, os

# helper function to generate error message
def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

# class/model-agnostic helper function to validate model instances
def validate_model_instance(model, id):
    if model == Task:
        model_name = "Task"
    elif model == Goal:
        model_name = "Goal"
    
    try:
        id = int(id)
    except:
        error_message(f"{model_name} #{id} invalid", 400)
    
    model_instance = model.query.get(id)

    if not model_instance:
        error_message(f"{model_name} #{id} not found", 404)
    
    return model_instance

# helper function to post completion message to slack
def post_slack_completion_message(task_id):
    task = validate_model_instance(Task, task_id)
    path = "https://slack.com/api/chat.postMessage"
    SLACK_API_KEY = os.environ.get("SLACK_BOT_TOKEN")

    request_headers = {"Authorization": f"Bearer {SLACK_API_KEY}"}
    request_body = {
        "channel": "C03EP2Q0WK1",
        "text": f"Someone just completed the task {task.title}"
    }

    requests.post(path, headers=request_headers, json=request_body)