from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.task import Task
# from app.models.task import tasks

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response_msg = {"message": f'{task_id} id is not valid, must be an integer'}
        abort(make_response(jsonify(response_msg), 400))
    the_task = Task.query.get(task_id)

    if the_task is None:
        response_msg = {"message": f'task with id {task_id} not found'}
        abort(make_response(jsonify(response_msg), 404))
    return the_task

@tasks_bp.route("", methods=["POST"])
def new_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    return make_response("201 CREATED", 201)

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():

    tasks_response = []
    tasks = Task.query.all()
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description
        })
    
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):

    task = validate_task_id(task_id)

    return jsonify({
        "id": task.task_id,
        "title": task.title,
        "description": task.description
        })
    return make_response({"message": f'task with id {task_id} not found'}, 404)

# @tasks_bp.route("", methods=["POST"])
# def create_task():
#     request_body = request.get_json()
#     new_task = Task(title=request_body["title"],
#                     description=request_body["description"]
#     )

#     db.session.add(new_task)
#     db.session.commit()

#     return make_response("CREATED", 201)

