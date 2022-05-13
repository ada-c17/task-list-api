from app import db
from app import helper_functions
from app.models.task import Task 
from datetime import datetime 
from flask import Blueprint, jsonify, make_response, request
import requests 
import os 

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    '''
    POST method to /tasks endpoint
    Input: title, description, and completed_at (which is optional - returns False if not entered)
    Returns: json response body with all input including id  
    '''
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    
    new_task = Task(title=request_body["title"], 
                    description=request_body["description"])

    if "completed_at" in request_body: 
        new_task.completed_at=request_body["completed_at"]
    
    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({"task": new_task.to_json()}), 201)


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    '''
    GET method to /tasks endpoint
    Returns: json response body with id, title, description, and completed_at from all tasks in /tasks endpoints 
    Can request to have titles sorted by ascending or descending order
    '''
    sort_order_query = request.args.get("sort")
    if sort_order_query == "desc":
            tasks = Task.query.order_by(Task.title.desc())
    elif sort_order_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    else:
        tasks = Task.query.all()
    
    tasks_response = [task.to_json() for task in tasks]
    return make_response(jsonify(tasks_response))

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    '''
    GET method to /tasks/<task_id> endpoint
    Returns: json response body with id, title, description, and completed_at from task with matching id
    '''
    task = helper_functions.validate_task(task_id)

    return make_response(jsonify({"task": task.to_json()}))

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    '''
    PUT method to /tasks/<task_id> endpoint
    Input: title and  description that needs to be updated
    Returns: json response body with all input, including id and completed_at, from task with matching id
    '''
    task = helper_functions.validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify({"task": task.to_json()}))


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_is_complete(task_id): 
    '''
    PATCH method to /tasks/<task_id>/mark_complete endpoint
    Input: sending a task with a specific id to mark_complete route will change the completed_at from None (which returns False)
    to True (by changing mark_complete to a datetime instance)
    Returns: json response body with id, title, description, and is_complete (datetime) and sends slack_bot message to slack
    channel task-notifications
    '''
    task = helper_functions.validate_task(task_id)
    task.completed_at = datetime.now()
    url = "https://slack.com/api/chat.postMessage"
    data_params = {
        "channel": "task-notifications", 
        "text": f"Someone just completed the task {task.title}"
    }
    slack_token = os.environ.get("SLACKBOT_API_KEY")
    header = {"Authorization": slack_token}
    # I never use response variable, but unsure how to do it otherwise
    response = requests.post(url, params=data_params, headers=header)

    db.session.commit()

    return make_response(jsonify({"task": task.to_json()}))

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_is_not_complete(task_id): 
    '''
    PATCH method to /tasks/<task_id>/mark_incomplete endpoint
    Input: sending a task with a specific id to mark_complete route will keep the completed_at parameter to None 
    (which returns False)
    Returns: json response body with id, title, description, and is_complete (False)
    '''
    task = helper_functions.validate_task(task_id)

    task.completed_at = None
    db.session.commit()

    return make_response(jsonify({"task": task.to_json()}))

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):    
    '''
    DELETE method to /tasks/<task_id> endpoint
    Input: sending a task with a specific id to will delete the task
    Returns: success message with specific task id and task title 
    '''
    task = helper_functions.validate_task(task_id)

    db.session.delete(task)
    db.session.commit()
    
    response = (f'Task {task.id} "{task.title}" successfully deleted')

    return make_response(jsonify({"details": response})) 
