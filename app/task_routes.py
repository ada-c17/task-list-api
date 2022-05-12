from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


# creates new task to the database
@tasks_bp.route("", methods=["POST"])
def create_task():
    # request_body = request.get_json()
    # new_task = Task(
    #     title=request_body["title"],
    #     description=request_body["description"]
    #     )

    # db.session.add(new_task)
    # db.session.commit()

    # return make_response(jsonify(f"Task {new_task.title} created"), 201)
    request_body = request.get_json()
    new_task = Task(
        title=request_body["title"],
        description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    response_body = {
        "task": new_task.make_dict()
    }
    return make_response(jsonify(response_body), 201)


# gets all saved tasks
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    response_body = [task.make_dict() for task in tasks]
    return make_response(jsonify(response_body), 200)