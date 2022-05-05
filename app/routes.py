from flask import Blueprint, request, jsonify, make_response, abort
from .models.task import Task
from app import db

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

def completed_or_not(response):
    complete = "is_complete"
    # [response] iterage in list of object, otherwise, TypeError
    if complete in [response]: 
        completed_status = True
    else:
        completed_status = False
    return completed_status

@task_bp.route("", methods=["POST"])
def create_tasks():
    response_body = request.get_json()
    
    new_task = Task(title=response_body["title"], description=response_body["description"])
    db.session.add(new_task)
    db.session.commit()
    
    completed_status = completed_or_not(response_body)
    return {
        "task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": completed_status
    }}, 201


@task_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    completed_status = completed_or_not(tasks)
    response_body = []
    for task in tasks:
        response_body.append({
            "id": task.task_id, 
            "title":task.title, 
            "description": task.description,
            "is_complete": completed_status
        })
    
    return jsonify(response_body), 200

def task_validation(taskID):
    try:
        taskID = int(taskID)
    except ValueError:
        rsp = {"msg": f"Invalid task id #{taskID}."}
        abort(make_response(jsonify(rsp), 400))
    
    valid_task = Task.query.get(taskID)
    
    if valid_task is None:
        rsp = {"msg": f"Given task #{taskID} is not found."}
        abort(make_response(jsonify(rsp), 404))

    return valid_task

@task_bp.route("/<taskID>", methods=["GET"])
def get_one_task(taskID):
    task_exist = task_validation(taskID)
    completed_status = completed_or_not(task_exist)

    rsp = {
        "task": {
        "id": task_exist.task_id,
        "title": task_exist.title,
        "description": task_exist.description,
        "is_complete": completed_status
    }}
    return jsonify(rsp), 200
    