from flask import Blueprint, request, make_response, abort, jsonify
from app import db
from app.models.task import Task
from sqlalchemy import desc, asc
from datetime import date, datetime
import os
import requests

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# Wave 1
# get all task list
@tasks_bp.route("", methods=["GET"])
def read_all_tasts():
    """
        - Returning all sorted tasks in json with 200
        - Returning empty list if no task in database
    """
    # sort all tasts by title
    params = request.args

    # sort tasks by id for specific goal id
    if "goal_id" in params and "sort" in params:
        if params["sort"].lower() == "desc" or params["sort"].lower() == "descending":
            id = params["goal_id"]
            chosen_task = Task.query.filter_by(goal_id=id).order_by(desc(Task.id)).all()
        else:
            chosen_task = Task.query.filter_by(goal_id=id).order_by(asc(Task.id)).all()
    # sort tasks by title
    elif "sort" in params:
        if params["sort"].lower() == "desc" or params["sort"].lower() == "descending":
                chosen_task = Task.query.order_by( desc(Task.title) ).all()
        else:
            chosen_task = Task.query.order_by( asc(Task.title) ).all()
        
    # filter by title
    elif "title" in params:
        task_title = params["title"]
        chosen_task = Task.query.filter_by(title=task_title).all()
    # no any query params will sort by id
    else:     
        chosen_task = Task.query.order_by(asc(Task.id)).all()

    # return empty list when no task in database
    if len(chosen_task) == 0:
        return jsonify([]), 200

    # get all tasts
    response_body = [task.task_response_body_dict() for task in chosen_task]

    return jsonify(response_body), 200



# helper function to check task id
def validate_task_id(task_id):
    """
    Checking the id task from input:
        - return object task if id is integer
        - raise exception if id is not integer then return status code 400,
        but if the id not exist then return status code 404

    """
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({"message": f"The task id {task_id} is invalid. The id must be integer."}, 400))
    
    tasks = Task.query.all()
    for task in tasks:
        if task.id == task_id:
            return task
    
    abort(make_response({"message": f"The task id {task_id} is not found"}, 404))


# get one task by id
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_task_by_id(task_id):
    """Getting a task by task id and return task object in json with 200"""
    chosen_task = validate_task_id(task_id)
    return jsonify({"task": chosen_task.task_response_body_dict()}), 200


# helper function to check key dictionary exist or not
def validate_input_key_for_post_or_update():
    """Checking missing data key when post or update
        - raise exception if the key doesn't exist
        - return request object if the key exist
    """
    request_task = request.get_json()
    if "title" not in request_task or "description" not in request_task:
        abort(make_response({"details": "Invalid data"}, 400))
    return request_task


# create one task
@tasks_bp.route("", methods=["POST"])
def creat_task():
    """Adding task into database and return task object in json with 201"""
    # validating input key whether missing or not
    request_task = validate_input_key_for_post_or_update()
    # creating new record in task table base on input
    new_task = Task(
        title = request_task["title"],
        description = request_task["description"]
    )
    # if input has completed_at then add it into database
    if "completed_at" in request_task :
        completed_date = datetime.strptime(request_task["completed_at"], "%a, %d %b %Y %H:%M:%S %Z").date()
        new_task.completed_at = completed_date
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.task_response_body_dict()}), 201


# update a task
@tasks_bp.route("<task_id>", methods=["PUT"])
def update_task(task_id):
    """Updating task by task id"""
    # validating task id
    chosen_task = validate_task_id(task_id)
    # validating input key whether it missing or not
    request_task = validate_input_key_for_post_or_update()
    # if title and description key not missing then update their values to database
    chosen_task.title = request_task["title"]
    chosen_task.description = request_task["description"]
   
    # if the request include completed_at key then update that value to database
    if "completed_at" in request_task:
        completed_date = datetime.strptime(request_task["completed_at"], "%a, %d %b %Y %H:%M:%S %Z").date()
        chosen_task.completed_at = completed_date
    db.session.add(chosen_task)
    db.session.commit()

    return jsonify({"task": chosen_task.task_response_body_dict()}), 200

# delete task by id
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task_by_id(task_id):
    """Removing a task by task id and return a message with 200"""
    # validating the task id
    chosen_task = validate_task_id(task_id)
    db.session.delete(chosen_task)
    db.session.commit()
    response_body = {"details": f'Task {task_id} "{chosen_task.title}" successfully deleted'}
    return jsonify(response_body), 200


# Wave 3
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_to_mark_complete(task_id):
    chosen_task = validate_task_id(task_id)
    request_task = request.get_json()
    if chosen_task.completed_at is None:
        chosen_task.completed_at = datetime.utcnow()

    db.session.commit()

    # post message to slack workspace
    SLACK_API_TOKEN = os.environ.get("SLACK_TOKEN")
    SLACK_PATH = "https://slack.com/api/chat.postMessage"
    MESSAGE = f"Someone just completed the task {chosen_task.title}"
    CHANNEL = "task-notifications"
    query_params = {
        "channel": CHANNEL,
        "text": MESSAGE
    }
    header = {
        "Authorization": SLACK_API_TOKEN
    }
    
    slack_response = requests.post(SLACK_PATH, params=query_params, headers=header)
    
    return jsonify({"task": chosen_task.task_response_body_dict()}), 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_to_mark_incomplete(task_id):
    chosen_task = validate_task_id(task_id)
    chosen_task.completed_at = None
    db.session.commit()
    return jsonify({"task": chosen_task.task_response_body_dict()}), 200