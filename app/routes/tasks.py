import re
from app import db
from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def handle_id_request(id):
    try:
        id = int(id)
    except:
        abort(make_response({"msg": f"Invalid Task ID '{id}'."}, 400))

    task = Task.query.get(id)

    if not task:
        abort(make_response({"msg": f"Task ID '{id}' does not exist."}, 404))

    return task

def check_complete_request_body(request):
    request_body = request.get_json()
    if all(element in request_body for element in Task.expected_elements):
        if all(type(request_body[element]) == Task.expected_elements[element] \
                    for element in Task.expected_elements):
                        return request_body
    abort(make_response({"details": "Invalid data"}, 400))


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    task_response = []
    task_list = Task.query.all()

    for task in task_list:
        task_response.append(task.make_response_dict())
    
    return make_response(jsonify(task_response), 200)

@tasks_bp.route("", methods=["POST"])
def create_new_task():
    request_body = check_complete_request_body(request)
    new_task = Task(
        title = request_body["title"],
        description = request_body["description"]
    )

    if request_body.get("completed_at"):
        new_task.completed_at = request_body["completed_at"]

    db.session.add(new_task)
    db.session.commit()

    confirmation_msg = {"task": new_task.make_response_dict()}

    return make_response(jsonify(confirmation_msg), 201)

@tasks_bp.route("/<id>", methods=["GET"])
def get_task_by_id(id):
    task = handle_id_request(id)
    confirmation_msg = {"task": task.make_response_dict()}
    return make_response(jsonify(confirmation_msg), 200)

@tasks_bp.route("/<id>", methods=["PUT"])
def update_task_by_id(id):
    request_body = check_complete_request_body(request)
    task_to_update = handle_id_request(id)

    task_to_update.title = request_body["title"]
    task_to_update.description = request_body["description"]

    db.session.commit()

    return make_response(
        jsonify({"task": task_to_update.make_response_dict()}),
        200
        )


@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task_by_id(id):
    task = handle_id_request(id)
    db.session.delete(task)
    db.session.commit()

    return make_response(
            jsonify({"details": f"Task {id} \"{task.title}\" successfully deleted"}), 
            200
            )