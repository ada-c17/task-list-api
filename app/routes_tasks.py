from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app.models.goal import Goal
from app import db
from datetime import datetime
import requests
import os

SLACK_PATH = "https://slack.com/api/chat.postMessage"
SLACK_KEY = os.environ.get("SLACK_API_KEY")

tasks_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response = {"details": f"{task_id} is not valid input."}
        abort(make_response(jsonify(response), 400))
    
    task = Task.query.get(task_id)

    if not task:
        response = {"details": f"Task {task_id} does not exist."}
        abort(make_response(jsonify(response), 404))
    
    return task

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    params = request.args
    if "sort" in params:
        if params["sort"] == "asc":
            tasks = Task.query.order_by(Task.title.asc()).all()
        elif params["sort"] == "desc":
            tasks = Task.query.order_by(Task.title.desc()).all()
        else:
            response = {"details": "Invalid data"}
            abort(make_response(jsonify(response), 400))
    # Get tasks that aren't completed yet   
    elif "complete" in params:
        if params["complete"] == "false":
            tasks = db.session.query(Task).filter(Task.completed_at == None)
        else:
            response = {"details": "Invalid data"}
            abort(make_response(jsonify(response), 400))
    # If there are no query params
    else:
        tasks = Task.query.all()
    
    response = [task.to_dict() for task in tasks]

    return jsonify(response), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)

    response = {
        "task": task.to_dict()
    }
    # Adds goal_id only if task has one
    if task.goal_id:
        response["task"]["goal_id"] = task.goal_id

    return jsonify(response), 200


@tasks_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()
    # Check minimum reqs for making a task: title and description
    try:
        new_task = Task(title=request_body["title"],
                description=request_body["description"])
    except:
        response = {"details": "Invalid data"}
        abort(make_response(jsonify(response), 400))
    
    # Check for optional attribute value of completed_at
    if request_body.get("completed_at"):
        try:
            # request object converts & changes datetime.utcnow() format
            # Example:
            # From datetime class- 2022-05-07 18:48:06.598253
            # To string class- 'Sat, 07 May 2022 23:59:31 GMT' 
            # I want my endpoint to accepted completed_at in either format
            completed_at = request_body["completed_at"] 
            # Converted string format will always start with a letter that is the day of the week
            if completed_at[0].isalpha():
                converted_datetime = datetime.strptime(completed_at, 
                    '%a, %d %B %Y %H:%M:%S %Z')
            else:
                # '2022-05-07 18:48:06.598253' format will never start with a letter
                #  I used this value to test in Postman, it is more accurate to datetime format
                converted_datetime = datetime.strptime(completed_at, 
                    '%Y-%m-%d %H:%M:%S.%f')
            new_task.completed_at = converted_datetime
        except: 
            # Again, any input is invalid that is not:
            # '2022-05-07 18:48:06.598253' 
            # 'Sat, 07 May 2022 23:59:31 GMT'
            response = {"details": "Invalid date data"}
            abort(make_response(jsonify(response), 400))

    db.session.add(new_task)
    db.session.commit()

    response = {
        "task": new_task.to_dict()
    }

    return jsonify(response), 201

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    # completed_at can only be changed by mark_(in)complete
    try:
        task.title = request_body["title"]
        task.description = request_body["description"]
    except:
        response = {"details": "Task needs both a title and description"}
        abort(make_response(jsonify(response), 400))

    db.session.commit()

    response = {
        "task": task.to_dict()
    }

    return jsonify(response), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    response = {
        "details": f'Task {task.task_id} "{task.title}" successfully deleted'
    }
    return jsonify(response), 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task_mark_complete(task_id):
    task = validate_task(task_id)

    # This route can mark a completed task as complete again
    if not task.completed_at:
        # I only want to change the value of completed_at when it is first complete
        task.completed_at = datetime.utcnow()
        db.session.commit()

        # Send Slack message only with first time task is completed
        headers = {
            "Authorization": f"Bearer {SLACK_KEY}"
        }
        query_params = {
            "format": "json",
            "channel": "task-notifications",
            "text": f"Someone just completed the task {task.title}"
        }
        requests.post(SLACK_PATH, headers=headers, params=query_params)

    response = {
        "task": task.to_dict()
    }

    return jsonify(response), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_task_mark_incomplete(task_id):
    task = validate_task(task_id)

    task.completed_at = None
    db.session.commit()

    response = {
        "task": task.to_dict()
    }

    return jsonify(response), 200
