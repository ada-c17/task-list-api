from flask import jsonify, abort, make_response
from .models.task import Task
from .models.goal import Goal
import requests, os

def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        error_message(f"task {task_id} invalid", 400)

    task = Task.query.get(task_id)

    if not task:
        error_message(f"task {task_id} not found", 404)

    return task

def post_completion_message_in_slack(task_id):
    task = validate_task(task_id)

    SLACK_PATH = "https://slack.com/api/chat.postMessage"
    SLACK_API_KEY = os.environ.get("SLACK_BOT_TOKEN")

    request_headers = {"Authorization": f"Bearer {SLACK_API_KEY}"}
    request_body = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }

    requests.post(SLACK_PATH, headers=request_headers, json=request_body)

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        error_message(f"goal {goal_id} invalid", 400)

    goal = Goal.query.get(goal_id)

    if not goal:
        error_message(f"goal {goal_id} not found", 404)

    return goal
