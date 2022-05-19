import os
from os import abort
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
import requests
from datetime import date
from dotenv import load_dotenv
load_dotenv()
from .helpers import validate_task

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

"""
--Added to helpers.py
"""
# def validate_task(task_id):
#     try:
#         task_id = int(task_id)
#     except:
#         abort(make_response({"message":f"task {task_id} invalid"}, 400))

#     task = Task.query.get(task_id)

#     if not task:
#         abort(make_response({"message":f"task {task_id} not found"}, 404))
    
#     return task


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

# # is this if statement necessary?
#     if not request_body["completed_at"]:
#         request_body["completed_at"] = 0

# I did a try and except here because when I use the if statement syntax above, it raises a key error because there is no completed_at in the request body
    try:
        request_body["completed_at"]
    except:
        request_body["completed_at"] = 0

# doesn't work like this.... not sure if my syntax is correct but also a key error because one of the keys doesn't exist in the request body 
    # if not request_body["description"] and not equest_body["title"]:
    #     return {"details": "Invalid data"}, 400

    try:
        request_body["description"]
        request_body["title"]
    except:
        return {"details": "Invalid data"}, 400

# same problem as above, key error raised because is_complete doesn't exist in the request body, is a try/except the only way around this?
    # if not request_body["is_complete"]:
    #     request_body["is_complete"] = False

    try:
        request_body["is_complete"]
    except:
        request_body["is_complete"] = False

    if request_body["completed_at"] != 0:
        # new_task = Task(title=request_body["title"],
        #                 description=request_body["description"],
        #                 completed_at= request_body["completed_at"],
        #                 is_complete=True)

# refactored to use my create class method in task.py
        new_task = Task.create(request_body)
        new_task.is_complete = True
        new_task.completed_at = request_body["completed_at"]

        db.session.add(new_task)
        db.session.commit()

        return new_task.to_json(), 201

    new_task = Task.create(request_body)
    
    db.session.add(new_task)
    db.session.commit()

    return new_task.to_json(), 201


"""
--refactored the get route to utilize my to_json method in my Task class by creating task_dict = task.to_json() and appending with "task" key in for loop
"""

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_request = request.args.get("sort")
    title_query = request.args.get("title")

    tasks = Task.query.all()
    
    if sort_request == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    if sort_request == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    if title_query:
        tasks = Task.query.filter_by(title=title_query)

    tasks_response = []
    for task in tasks:
        task_dict = task.to_json()
        tasks_response.append(
        #     {
        #         "id": task.task_id,
        #         "title": task.title,
        #         "description": task.description,
        #         "is_complete": task.is_complete
        #     }
        task_dict["task"]
        )
            


    return jsonify(tasks_response)



@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)

    # task_goal_dict = {
    #     "task": {
    #         "id": task.task_id,
    #         "title": task.title,
    #         "description": task.description,
    #         "is_complete": task.is_complete
    #     }
    # }

    task.to_json()
    
    if not task.goal_id:
        # return task_goal_dict
        return task.to_json()
    else:
        
        # task_goal_dict["task"]["goal_id"] = task.goal_id
        # return task_goal_dict

        task_goal_dict = task.to_json()
        task_goal_dict["task"]["goal_id"] = task.goal_id
        return task_goal_dict
    
            

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    if task.completed_at:
        task.is_complete = True

    db.session.commit()

    # return {
    #     "task": {
    #         "id": task.task_id,
    #         "title": task.title,
    #         "description": task.description,
    #         "is_complete": task.is_complete
    #     }
    # }

    return task.to_json()

    


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}



@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_is_complete(task_id):
    task = validate_task(task_id)

    task.is_complete = True
    task.completed_at = date.today() 
    
    db.session.commit()

    path = "https://slack.com/api/chat.postMessage"
    API_KEY = os.environ.get("SLACK_API_KEY")
    header = {"Authorization": API_KEY}
    query_params = {
        "channel": "task-notifications",
        "text": "Someone just completed the task"
    }

    requests.post(path, headers=header, params=query_params)

    # return {
    #     "task": {
    #         "id": task.task_id,
    #         "title": task.title,
    #         "description": task.description,
    #         "is_complete": task.is_complete
    #     }
    # }, 200

    return task.to_json(), 200



@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_is_incomplete(task_id):
    task = validate_task(task_id)

    task.completed_at = None 

    db.session.commit()

    # return {
    #     "task": {
    #         "id": task.task_id,
    #         "title": task.title,
    #         "description": task.description,
    #         "is_complete": task.is_complete
    #     }
    # }, 200

    return task.to_json(), 200
