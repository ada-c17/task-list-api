from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from .helpers import validate


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# POST ROUTES


@tasks_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    new_task = Task(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task": new_task.to_json()}, 201)

# GET ROUTES


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    # moons_query = request.args.get("moons")
    # description_query = request.args.get("description")

    # if moons_query:
    #     tasks = Planet.query.filter_by(moons=moons_query)
    # elif description_query:
    # planets = Planet.query.filter_by(description=description_query)
    # else:
    tasks = Task.query.all()

    response = [task.to_json() for task in tasks]

    return jsonify(response), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate(task_id)
    return make_response({"task": task.to_json()}, 200)

# PUT ROUTES


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate(task_id)
    request_body = request.get_json()

    task.update(request_body)

    db.session.commit()

    return make_response({"task": task.to_json()}, 200)

# DELETE ROUTES


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_planet(task_id):
    task = validate(task_id)
    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task_id} \"{task.title}\" successfully deleted"}, 200)
