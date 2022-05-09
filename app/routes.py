from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.task import Task
from sqlalchemy import asc, desc
import json

# creating task with using POST in our route decorator
task_bp = Blueprint("tasks", __name__, url_prefix = "/tasks")
@task_bp.route("", methods = ["POST"])
def create_task(): 
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return jsonify({"details": "Invalid data"}), 400
    
    new_task = Task(title= request_body["title"],
                    description = request_body["description"])
    db.session.add(new_task)
    db.session.commit()
    response_body = {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": bool(new_task.completed_at)
        }
    }
    return make_response(jsonify(response_body)), 201
        
#validating task and using as a helper function in other functions
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response = ({"details": "Invalid data"})
        abort(make_response(jsonify(response), 400))
        
    chosen_task = Task.query.get(task_id)
    if not chosen_task:
        response = ({'details': f"Could not find task"})
        abort(make_response(jsonify(response), 404))
        
    return chosen_task


#get all task by using GET in route decorater 
@task_bp.route("", methods = ["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(asc(Task.title))
    elif sort_query == "desc":
        tasks = Task.query.order_by(desc(Task.title))
    else:
        tasks = Task.query.all()
    
    response = []
    for task in tasks:
        if task == None or task == "": 
            pass
        response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)}) 
        
    return jsonify(response), 200


#get one task by using GET in route decorater and aaccessing id
@task_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):
    chosen_task = validate_task(task_id)
    chosen_task = {
        "task":{
            "id": chosen_task.task_id,
            "title": chosen_task.title,
            "description": chosen_task.description,
            "is_complete": bool(chosen_task.completed_at)
            }
    }
    return jsonify(chosen_task), 200


#updating task by using PUT in route decorater
@task_bp.route("/<task_id>", methods = ["PUT"])
def replace_one_task(task_id):
    request_body = request.get_json()
    chosen_task = validate_task(task_id)
    chosen_task.title = request_body["title"]
    chosen_task.description = request_body["description"]
        
    db.session.commit()
    response_body = {
        "task": {
            "id": chosen_task.task_id,
            "title": chosen_task.title,
            "description": chosen_task.description,
            "is_complete": bool(chosen_task.completed_at)
            }
        }
    return jsonify(response_body), 200

#deleting task by using DELETE in rout and by accessing task id
@task_bp.route("/<task_id>", methods = ["DELETE"])
def delete_one_task(task_id):
    chosen_task = validate_task(task_id)
    
    db.session.delete(chosen_task)
    db.session.commit()
    response_body = {"details": f'Task {task_id} \"Go on my daily walk 🏞\" successfully deleted'}
    return jsonify(response_body), 200
