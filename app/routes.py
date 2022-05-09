import json
from crypt import methods
from flask import Blueprint, abort, make_response, jsonify, request
#from requests import request
from app.models.task import Task
from app import db

task_bp = Blueprint('task_bp', __name__, url_prefix="/tasks")


@task_bp.route('', methods=['POST'])
def create_one_task():
    request_body = request.get_json()
    try:
        request_body["title"] == True
        request_body["description"] == True
    except KeyError:
        rsp = {"details": "Invalid data"}
        abort(make_response(jsonify(rsp), 400))

    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
    )
    
    db.session.add(new_task)
    db.session.commit()

    if new_task.completed_at is None:
        new_task.completed_at = False

    rsp = {"task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": new_task.completed_at
    }}
    return jsonify(rsp), 201


def get_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        rsp = {"msg": f"Invalid ID: {task_id}"}
        abort(make_response(jsonify(rsp), 400))    
    
    selected_task = Task.query.get(task_id)
    if selected_task is None:
        rsp = {"msg": f"Could not find task with ID: {task_id}"}
        abort(make_response(jsonify(rsp), 404))

    return selected_task    


@task_bp.route('/<task_id>', methods=['GET'])
def get_or_update_one_task(task_id):
    selected_task = get_task_or_abort(task_id)

    if selected_task.completed_at is None:
        selected_task.completed_at = False

    rsp = {
        "task": {
            "id": selected_task.task_id,
            "title": selected_task.title,
            "description": selected_task.description,
            "is_complete": selected_task.completed_at
        }
    }
    return jsonify(rsp), 200


@task_bp.route('', methods=['GET'])
def get_all_tasks():
    tasks = Task.query.all()
    tasks_response = []

    for task in tasks:
        if task.completed_at is None:
            task.completed_at = False
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at
        })

    return jsonify(tasks_response), 200    

@task_bp.route('/<task_id>', methods=['PUT'])
def update_one_task(task_id):
    selected_task = get_task_or_abort(task_id)
    request_body = request.get_json()
    try:
        selected_task.title = request_body["title"]
        selected_task.description = request_body["description"]
    except KeyError:
        return {"details": "Invalid data"}, 400   
    db.session.commit()

    if selected_task.completed_at is None:
        selected_task.completed_at = False

    rsp = {
        "task": {
            "id": selected_task.task_id,
            "title": selected_task.title,
            "description": selected_task.description,
            "is_complete": selected_task.completed_at
        }
    }
    return jsonify(rsp), 200

@task_bp.route('/<task_id>', methods=['DELETE'])
def delete_one_task(task_id):
    selected_task = get_task_or_abort(task_id)

    db.session.delete(selected_task)
    db.session.commit()

    return {
        "details": 
        f'Task {selected_task.task_id} \"{selected_task.title}" successfully deleted'}, 200