from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()
    new_task = Task(
        title=request_body["title"],
        description=request_body["description"]
    )

    try:
        new_task.title = request_body["title"]
        new_task.description = request_body["description"]
    
    except KeyError:
        return {
            "details": "Invalid data"
        } , 400

    db.session.add(new_task)
    db.session.commit()
    
    response = jsonify({"task": {
        "id": new_task.task_id,
                "title": new_task.title,
                "description": new_task.description,
                "is_complete": new_task.completed_at}
    })
    return response, 201

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    params = request.args
    if "title" in params:
        title_name = params["title"]
        tasks = Task.query.filter_by(title=title_name)
    elif "description" in params:
        description_name = params["description"]
        tasks = Task.query.filter_by(description=description_name)
    elif "completed_at" in params:
        completed_at_time = params["completed_at"]
        tasks = Task.query.filter_by(completed_at=completed_at_time)
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.completed_at
            }
        )
    return jsonify(tasks_response)

def get_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response = {"message": f"Invalid id: {task_id}"}
        abort(make_response(jsonify(response),400))
    chosen_task = Task.query.get(task_id)

    if chosen_task is None:
        response = {"message": f"Could not find planet with id #{task_id}"}
        abort(make_response(jsonify(response),404))
    return chosen_task

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    chosen_task = get_task_or_abort(task_id)
    response = {
        "id": chosen_task.task_id,
        "title": chosen_task.title,
        "description": chosen_task.description,
        "is_complete": chosen_task.completed_at
    }

    return jsonify(response),200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def replace_task(task_id):
    chosen_task = get_task_or_abort(task_id)
    request_body = request.get_json()

    try:
        chosen_task.title = request_body["title"]
        chosen_task.description = request_body["description"]
        #chosen_task.cpmleted_at = request_body["is_complete"]
    
    except KeyError:
        return {
            "message": "title, description are required"
        } , 400

    db.session.commit()
    response = jsonify({"task": {
        "id": chosen_task.task_id,
                "title": chosen_task.title,
                "description": chosen_task.description,
                "is_complete": chosen_task.completed_at}
    })
    return response, 200

    # return {
    #     "message": f"task #{chosen_task.task_id} successfully replaced"
    # }, 200

@tasks_bp.route("/<task_id>", methods = ["DELETE"])
def delete_task(task_id):
    chosen_task = get_task_or_abort(task_id)
    db.session.delete(chosen_task)
    db.session.commit()

    return {
        "details": f'Task {chosen_task.task_id} "{chosen_task.title}" successfully deleted'
    }, 200