import json
from os import abort
from xmlrpc.client import DateTime
from attr import validate
from sqlalchemy import true
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from tests.conftest import one_task


# ---- CREATING BLUEPRINT INSTANCE---- # 
tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


# ---- HELPER FUNCTIONS ---- #


def validate_task(task_id):
    # Check if task_id is a valid integer
    try:
        task_id = int(task_id)
    except:
        # If it's not, 400 response code
        abort(make_response({"message" : f"Task {task_id} is invalid."}, 400))

    # Search for this task_id in the Task Blueprint
    task = Task.query.get(task_id)

    # If this specific task isn't found, 404 response code
    if not task:
        abort(make_response({"message" : f"This task is not found."}, 404))
    # If task found, return it 
    return task




# ---- ROUTE FUNCTIONS ---- #

# class Task(db.Model):
#     task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     title = db.Column(db.String)
#     description = db.Column(db.String)
#     completed_at = db.Column(db.DateTime, nullable=True)




# ---- GET ALL TASKS ---- #
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    
    tasks_response = []

    tasks = Task.query.all()

    for task in tasks:
        if task.completed_at == None:
            tasks_response.append(
                {
                    "id" : task.task_id,
                    "title" : task.title,
                    "description" : task.description,
                    "is_complete" : False
                }
            )
        else:
            tasks_response.append(
                {
                    "id" : task.task_id,
                    "title" : task.title,
                    "description" : task.description,
                    "is_complete" : True
                }
            )

    # return make_response({"task": tasks_response}, 201)
    # return {"tasks": tasks_response}, 201
    return jsonify(tasks_response)




# ---- GET ONE TASK BY ID ---- #
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)

    return jsonify({"task" : 
        {
            "id" : task.task_id,
            "title" : task.title,
            "description" : task.description,
            "is_complete" : False
        }
    })




# ---- CREATE A TASK ---- #
@tasks_bp.route("", methods=["POST"])
def create_task():
    
    request_body = request.get_json()

    if not "title" in request_body or not "description" in request_body:
        return jsonify({
            "details" : "Invalid data"
        }), 400


    new_task = Task(title=request_body["title"],
                    description=request_body["description"])


    db.session.add(new_task)
    db.session.commit()

    response_body = jsonify({"task" : 
        {
            "id" : new_task.task_id,
            "title" : new_task.title,
            "description" : new_task.description,
            "is_complete" : False
        }
    })

    return response_body, 201



# ---- UPDATE A TASK ---- #
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    
    task_to_update = validate_task(task_id)

    request_body = request.get_json()

    task_to_update.title = request_body["title"]
    task_to_update.description = request_body["description"]

    db.session.commit()

    response_body = jsonify({"task" : 
        {
            "id" : task_to_update.task_id,
            "title" : task_to_update.title,
            "description" : task_to_update.description,
            "is_complete" : False
        }
    })

    return response_body, 200




# ---- DELETE ONE TASK ---- #
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):

    verified_task = validate_task(task_id)

    if verified_task:
        task_to_delete = Task.query.get(task_id)


    db.session.delete(task_to_delete)
    # Commit the changes
    db.session.commit()

    # Need to change this response body  
    return {
        "details": f'Task {task_id} \"{task_to_delete.title}\" successfully deleted'
    }, 200

    # {
    #     "details": 'Task 1 "Go on my daily walk 🏞 " successfully deleted'
    # }