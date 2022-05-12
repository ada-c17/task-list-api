import json
from crypt import methods
from flask import Blueprint, abort, make_response, jsonify, request
from datetime import datetime
from app.models.task import Task
from app import db

task_bp = Blueprint('task_bp', __name__, url_prefix="/tasks")

# helper function to determine true or false
# ....actually might need to change this once datetime comes into play
def boolean_completed_task(task):
    if task.completed_at is None:
        task.completed_at = False
    else:
        task.completed_at = True


@task_bp.route('', methods=['POST'])
def create_one_task():
    request_body = request.get_json()
    try:
        request_body["title"] == True
        request_body["description"] == True
    except KeyError:
        rsp = {"details": "Invalid data"}
        abort(make_response(jsonify(rsp), 400))

    if 'completed_at' in request_body:
        new_task = Task(
            title = request_body["title"],
            description = request_body["description"],
            completed_at = request_body["completed_at"]
        )
    else:
        new_task = Task(
            title = request_body["title"],
            description = request_body["description"],
        )
    

    db.session.add(new_task)
    db.session.commit()

    boolean_completed_task(new_task)

    rsp = {"task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": new_task.completed_at
    }}
    
    return jsonify(rsp), 201


def validate_task(task_id):
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
    selected_task = validate_task(task_id)

    boolean_completed_task(selected_task)
    
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
    sort_tasks = request.args.get("sort")

    tasks = Task.query.all()
    tasks_response = []

    

    for task in tasks:
        boolean_completed_task(task)  
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at
        })
    if sort_tasks:
        if sort_tasks == "asc":
            return jsonify(sorted(tasks_response, key=lambda a: a["title"])), 200
        elif sort_tasks == "desc":
            return jsonify(sorted(tasks_response, key=lambda a: a["title"], reverse=True)), 200
    return jsonify(tasks_response), 200    

@task_bp.route('/<task_id>', methods=['PUT'])
def put_one_task(task_id):
    selected_task = validate_task(task_id)
    request_body = request.get_json()
    try:
        selected_task.title = request_body["title"]
        selected_task.description = request_body["description"]
    except KeyError:
        return {"details": "Invalid data"}, 400   
    db.session.commit()

    boolean_completed_task(selected_task)
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
    selected_task = validate_task(task_id)

    db.session.delete(selected_task)
    db.session.commit()

    return {
        "details": 
        f'Task {selected_task.task_id} \"{selected_task.title}" successfully deleted'}, 200


# frankly, I'd love to be able to merge this function 
# and the one below into a singular funct. and just use two route decorators
# until I can figure that out though, I'm separating them into two
@task_bp.route('/<task_id>/mark_complete', methods=['PATCH'])
def mark_task_complete(task_id):
    selected_task = validate_task(task_id)

    selected_task.completed_at = datetime.utcnow()
    db.session.commit()

    boolean_completed_task(selected_task)
    rsp = {
        "task": {
            "id": selected_task.task_id,
            "title": selected_task.title,
            "description": selected_task.description,
            "is_complete": selected_task.completed_at
        }
    }
    return jsonify(rsp), 200

# ditto above
@task_bp.route('/<task_id>/mark_incomplete', methods=['PATCH'])
def mark_task_incomplete(task_id):
    selected_task = validate_task(task_id)
    
    selected_task.completed_at = None
    db.session.commit()

    boolean_completed_task(selected_task)
    rsp = {
        "task": {
            "id": selected_task.task_id,
            "title": selected_task.title,
            "description": selected_task.description,
            "is_complete": selected_task.completed_at
        }
    }
    return jsonify(rsp), 200
