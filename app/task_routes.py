from datetime import datetime
# from http import client
from app import db
from flask import Blueprint, jsonify, make_response, request, abort
from app.models.task import Task
from sqlalchemy import desc, asc, select
import requests, os




#instantiate blueprint
task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#helper functions
#validate task id is int(id) or throw 400 for non int or 404 for int(id) not found
def validate_task_id(task_key):
    try:
        task_key = int(task_key)
    except:
        abort(make_response(dict(message=f"Task {task_key} is not an int."), 400))
    
    task = Task.query.get(task_key)
    if not task:
        return abort(make_response(dict(message=f"Task {task_key} is invalid."), 404))
    else:
        return task

#POST to SlackBot
def post_to_slack(task_key):
    client = os.environ.get("SLACK_API_AUTH")
    

    url = "https://slack.com/api/chat.postMessage"

    headers = {"Authorization" : f"Bearer {client}"}
    
    data = {
        "channel" : "C03FFV84GM7",
        "text" : f"Someone just completed the task {task_key.title}"
    }

    response = requests.post(url, headers=headers, data=data)

    response_body = response.json()

    return response_body


#CREATE/POST a task
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
        
    try:    
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"],
        )
        #make sure completed_at is in request body
        #update new task value to what was given at request body
        #refactored for wave 3

        if "completed_at" in request_body:
            new_task.completed_at = request_body["completed_at"]
        db.session.add(new_task)
        db.session.commit()
        return new_task.to_dict(), 201
    except KeyError:
        return (dict(details=f"Invalid data"), 400)


#READ/GET all tasks return 201 or 200 or 200 []
@task_bp.route("", methods=["GET"])
def get_all_tasks():
        tasks_response = []

        title_query = request.args.get("title")
        title_sort = request.args.get("sort")
        description_query = request.args.get("description")
        completed_at_query = request.args.get("completed_at")
        is_complete_query = request.args.get("is_complete_query")
    
        #filter by title key
        if title_sort == "asc":
            tasks = Task.query.order_by(Task.title.asc())
        elif title_sort == "desc":
            tasks = Task.query.order_by(Task.title.desc())
        elif title_query:
            tasks = Task.query.filter_by(title=title_query)
        elif description_query:
            tasks = Task.query.filter_by(description=description_query)
        elif completed_at_query:
            tasks = Task.query.filter_by(completed_at=completed_at_query)
        elif is_complete_query:
            tasks = Task.query.filter_by(is_complete=is_complete_query)
        else:
            tasks = Task.query.all()

        for task in tasks:
            task_object = task.to_dict()
            tasks_response.append(task_object["task"])
        
        return jsonify(tasks_response), 200

#PATCH route for complete task
@task_bp.route("/<task_key>/mark_complete", methods=["PATCH"])
def mark_task_complete_by_id(task_key):
    
    #validate task id
    task = validate_task_id(task_key)


    task.completed_at = datetime.now()
        

    db.session.commit()

    #POST to Slack with SlackBot after marked complete
    post_to_slack(task)

    return jsonify(task.to_dict()), 200

#PATCH route for incomplete task
@task_bp.route("/<task_key>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete_by_id(task_key):

    #validate task id
    task = validate_task_id(task_key)

    #if task has a datetime value, changed completed_at to None
    task.completed_at = None

    db.session.commit()

    #response body
    return jsonify(task.to_dict()), 200


#GET/READ one task by id
@task_bp.route("/<task_key>", methods=["GET"])
def get_one_task_by_id(task_key):
    task = validate_task_id(task_key)

    if task.goal_key:
        return jsonify(task.dict_rel()), 200
    

    return jsonify(task.to_dict()), 200


#REPLACE ALL OF/PUT task
#this endpoint will update the created_at attribute wave 3
@task_bp.route("/<task_key>", methods=["PUT"])
def replace_task_by_id(task_key):
    task = validate_task_id(task_key)
    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return jsonify(task.to_dict()), 200

#DELETE a task by id
@task_bp.route("/<task_key>", methods=["DELETE"])
def delete_task_by_id(task_key):
    task = validate_task_id(task_key)

    db.session.delete(task)
    db.session.commit()

    return make_response(dict(details=f'Task {task.task_id} "{task.description}" successfully deleted'), 200)



