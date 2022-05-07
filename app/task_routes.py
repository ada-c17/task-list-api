
from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
import datetime as dt
from datetime import date
import os
import requests

task_bp = Blueprint("Tasks", __name__, url_prefix="/tasks")

# Helper functions

def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

def success_message(message, status_code=200):
    return make_response(jsonify(message), status_code)

def return_database_info_list(return_value):
    return make_response(jsonify(return_value))

def return_database_info_task(return_value):
    return make_response(jsonify(dict(task=return_value)))

def get_task_by_id(id):
    try:
        id = int(id)
    except ValueError:
        error_message(f"Invalid id: {id}", 400)
    task = Task.query.get(id)
    if task:
        return task
    else:
        error_message(f"Task id: {id} not found", 404)

def create_task_safely(data_dict):
    try:
        return Task.create_from_dict(data_dict)
    except ValueError as err:
        error_message(f"Invalid data", 400)
    except KeyError as err:
        error_message(f"Missing key(s): {err}.  Task not added to Task List.", 400)

def update_task_safely(task, data_dict):
    try:
        task.update_self(data_dict)
    except ValueError as err:
        error_message(f"Invalid key(s): {err}. Task not updated.", 400)
    except KeyError as err:
        error_message(f"Missing key(s): {err}. Task not updated.", 400)

def send_slackbot_message(title):
    path = "https://slack.com/api/chat.postMessage"
    slackbot_key = os.environ.get("SLACK_OAUTH_TOKEN")
    headers = {'authorization': 'Bearer ' + slackbot_key}
    params = {
        'channel' : 'task-notifications',
        'text' : f'Someone just completed task {title}! :tada::tada::tada:',
    }
    requests.patch(path, headers=headers, params=params)



# Route functions

@task_bp.route("", methods=["POST"])
def create_new_task():
    request_body = request.get_json()
    new_task = create_task_safely(request_body)

    db.session.add(new_task)
    db.session.commit()

    return success_message(dict(task=new_task.self_to_dict()), 201)

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_param = request.args.get("sort")
    tasks = Task.query.all()
    all_tasks = [task.self_to_dict() for task in tasks]
    if not sort_param:
        return return_database_info_list(all_tasks)
    if sort_param == "asc":
        sorted_tasks_asc = sorted(all_tasks, key = lambda i : i["title"])
        return return_database_info_list(sorted_tasks_asc)
    if sort_param == "desc":
        sorted_tasks_desc = sorted(all_tasks, key = lambda i : i["title"], reverse=True)
        return return_database_info_list(sorted_tasks_desc)


@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = get_task_by_id(task_id)

    return return_database_info_task(task.self_to_dict())

@task_bp.route("/<task_id>", methods=["PUT", "PATCH"])
def update_task_by_id(task_id):
    task = get_task_by_id(task_id)

    request_body = request.get_json()
    update_task_safely(task, request_body)

    db.session.commit()

    return return_database_info_task(task.self_to_dict())

@task_bp.route("/<task_id>/<completion_status>", methods=["PATCH"])
def complete_task_by_id(task_id, completion_status):
    task = get_task_by_id(task_id)

    if completion_status == "mark_complete":
        completion_info = {
            "completed_at" : dt.date.today()
        }
        send_slackbot_message(task.title)
    elif completion_status == "mark_incomplete":
        completion_info = {
            "completed_at" : None
        }
    update_task_safely(task, completion_info)

    db.session.commit()

    return return_database_info_task(task.self_to_dict())


@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = get_task_by_id(task_id)

    db.session.delete(task)
    db.session.commit()

    return success_message(dict(details=f'Task {task.task_id} "{task.title}" successfully deleted'))