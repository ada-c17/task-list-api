from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app import db

tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')

@tasks_bp.route('', methods=['POST'])
def create_one_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                description=request_body["description"])
        
    db.session.add(new_task)
    db.session.commit()
    return jsonify(
        {"id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": bool(new_task.completed_at)
    }), 201
    
def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"Task {task_id} invalid.  Must be numerical"}, 400))
        
    task = Task.query.get(task_id)

    if task is None:
        abort(make_response({"message": f"Task {task_id} not found"}, 404))
        
    return task

@tasks_bp.route('', methods=['GET'])
def get_all_tasks():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        })
    return jsonify(tasks_response)
            


@tasks_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    chosen_task = validate_task_id(task_id)
    rsp = {
        'task id': chosen_task.task_id,
        'title': chosen_task.title,
        'description': chosen_task.description,
        'is_complete': bool(chosen_task.completed_at)
    }
    return jsonify(rsp), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        rsp = {"msg": f"Invalid id: {task_id}"}
        return jsonify(rsp), 400
    
    chosen_task = Task.query.get(task_id)
    if chosen_task is None:
        rsp = {"msg": f"Could not find task with id {task_id}"}
        return jsonify(rsp), 404

    db.session.delete(chosen_task)
    db.session.commit()

    return {
        "msg": f"Task #{chosen_task.id} successfully deleted"
    }, 200