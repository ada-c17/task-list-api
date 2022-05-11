from flask import Blueprint, jsonify, request, make_response
from app import db
from app.models.task import Task
from .helper import validate_client_requests, validate_task



tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#Get all 
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    title_sorted_query = request.args.get("sort")
    if title_sorted_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif title_sorted_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())

    return jsonify(tasks_response),200


#Get one
@tasks_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_task(id)

    return {"task": task.to_json()}, 200


#Create one
@tasks_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()
    new_task = validate_client_requests(request_body)
    db.session.add(new_task)
    db.session.commit()
    return {"task": new_task.to_json()}, 201
    
    # or without helper function:
    #request_body = request.get_json()
    #if "title" in request_body and "description" in request_body:
    #     new_task = Task.create(request_body)
    #     db.session.add(new_task)
    #     db.session.commit()
    # else:
    #     return  {"details": "Invalid data"}, 400
    

#Update one
@tasks_bp.route("/<id>", methods=["PUT"])
def update_one_task(id):
    task = validate_task(id)
    request_body = request.get_json()
    task.update(request_body)
    db.session.commit()
    return {"task": task.to_json()}, 200


#Delete one
@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_one_task(id):
    task = validate_task(id)
    db.session.delete(task)
    db.session.commit()
    return {"details": f'Task {id} "Go on my daily walk 🏞" successfully deleted'}


