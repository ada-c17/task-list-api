from flask import Blueprint, jsonify, make_response, abort, request
from app.models.task import Task
from app import db
from datetime import datetime
from app.external import slack

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

#Create task
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    try:
        title = request_body['title']
        description = request_body['description']
    except KeyError:
        return abort(make_response({"details": 'Invalid data'}, 400))

    new_task = Task(
        title = title, 
        description = description,
        completed_at = request_body.get("completed_at")
    )

    db.session.add(new_task)
    db.session.commit()

    response = {
        "task": new_task.to_json()
    }

    return make_response(jsonify(response), 201)


#Get all tasks or no saved tasks
@task_bp.route("", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    
    sort_query = request.args.get("sort") 
    if sort_query == "asc":
        tasks = sorted(tasks, key=lambda task: task.title)
    elif sort_query == "desc":
        tasks = sorted(tasks, key=lambda task: task.title, reverse=True)

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())

    return make_response(jsonify(tasks_response), 200)

#Get One Task: One Saved Task
@task_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return abort(make_response({"message": f"Task {task_id} is not found"}, 404))

    response = {
        "task": task.to_json()
    }

    return jsonify(response)

#Update one task
@task_bp.route("/<task_id>", methods = ["PUT"])
def update_one_tasks(task_id):
    task = Task.query.get(task_id)

    if not task:
        return abort(make_response({"message": f"Task {task_id} is not found"}, 404))

    request_body = request.get_json()

    task.title = request_body['title']
    task.description = request_body['description']

    if 'completed_at' in request_body:
        task.completed_at = request_body['completed_at']

    db.session.commit()

    return make_response(jsonify({"task": task.to_json()}), 200)

#Delete Task: Deleting a Task
@task_bp.route("/<task_id>", methods = ["DELETE"])
def delete_one_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return abort(make_response({"message": f"Task {task_id} is not found"}, 404))

    db.session.delete(task)
    db.session.commit()

    response = {
        'details': f'Task {task.task_id} "{task.title}" successfully deleted'
    }

    return make_response(response, 200)

@task_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
def mark_complete(task_id):
    task = Task.query.get(task_id)

    if not task:
        return abort(make_response({"message": f"Task {task_id} is not found"}, 404))

    task.completed_at = datetime.now()
    db.session.commit()

    slack.notify_completed(task.title)

    return make_response(jsonify({
        "task": task.to_json()
    }), 200)

@task_bp.route("/<task_id>/mark_incomplete", methods = ["PATCH"])
def mark_incomplete(task_id):
    task = Task.query.get(task_id)

    if not task:
        return abort(make_response({"message": f"Task {task_id} is not found"}, 404))

    task.completed_at = None
    db.session.commit()

    return make_response(jsonify({
        "task": task.to_json()
    }), 200)
