from urllib import response
from flask import Blueprint, jsonify, make_response, abort, request
from app.models.task import Task
from app import db


task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@task_bp.route("", methods=["GET"])
def get_all_tasks():
    task_response_body = []
    tasks = Task.query.all()

    for task in tasks:
        task_response_body.append(task.to_json())

    return jsonify(task_response_body), 200

@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    print(request_body)
    
    try:
        new_task = Task.create(request_body)
    except KeyError:
        return {"details": "Invalid data"}, 400

    db.session.add(new_task)
    db.session.commit()

    response_body = {}
    response_body["task"] = new_task.to_json()
    return jsonify(response_body), 201



@task_bp.route("/<id>", methods = ["GET"])
def get_one_tasks(id):
    one_task = Task.validate(id)
    response_body = {}
    response_body["task"] = one_task.to_json()

    return jsonify(response_body), 200

@task_bp.route("/<id>", methods = ["PUT"])
def update_task(id):
    one_task = Task.validate(id)
    request_body = request.get_json()

    one_task.update(request_body)

    db.session.commit()
    response_body = {}
    response_body["task"] = one_task.to_json()

    return jsonify(response_body), 200

@task_bp.route("/<id>", methods = ["DELETE"])
def delete_task(id):
    one_task = Task.validate(id)
    db.session.delete(one_task)
    db.session.commit()

    return jsonify({"details": f'Task {one_task.task_id} "{one_task.title}" successfully deleted'})





