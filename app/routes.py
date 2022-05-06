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
    return jsonify({ 'task':
        {"id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": new_task.is_complete}
    }), 201
    
def get_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        rsp = {"msg": f"Invalid id: {task_id}"}
        abort(make_response(jsonify(rsp), 400))
    chosen_cat = Task.query.get(task_id)

    if chosen_cat is None:
        rsp = {"msg": f"Could not find task with id {task_id}"}
        abort(make_response(jsonify(rsp), 404))
    return chosen_cat

@tasks_bp.route('', methods=['GET'])
def get_all_tasks():
    params = request.args
    if "title" in params and "description" in params:
        title_name = params["title"]
        description_value = params["description"]
        cats = Task.query.filter_by(title=title_name, description=description_value)
    elif "title" in params:
        title_name = params["title"]
        tasks = Task.query.filter_by(title=title_name)
    elif "completed_at" in params:
        completed_at_value = params["completed at"]
        tasks = Task.query.filter_by(completed_at=completed_at_value)
    else:
        tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            'id': task.task_id,
            'title': task.title,
            'description': task.description,
            'completed_at': task.completed_at
        })
    return jsonify(tasks_response)

def get_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        rsp = {"msg": f"Invalid id: {task_id}"}
        abort(make_response(jsonify(rsp), 400))
    chosen_task = Task.query.get(task_id)

    if chosen_task is None:
        rsp = {"msg": f"Could not find task with id {task_id}"}
        abort(make_response(jsonify(rsp), 404))
    return chosen_task

@tasks_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    chosen_task = get_task_or_abort(task_id)
    rsp = {
        'task id': chosen_task.task_id,
        'title': chosen_task.title,
        'description': chosen_task.description,
        'is_complete': chosen_task.is_complete
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