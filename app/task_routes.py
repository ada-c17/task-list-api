from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# helper functions
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"error": f"Task id invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"error":f"Task not found"}, 404))

    return task

# creates new task to the database
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return make_response(jsonify({"details": "Invalid data"}), 400)
        
    new_task = Task(
        title=request_body["title"],
        description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    response_body = {
        "task": new_task.make_dict()
    }
    return make_response(jsonify(response_body), 201)


# get all saved tasks
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    response_body = [task.make_dict() for task in tasks]
    return make_response(jsonify(response_body), 200)


# get one task by task id 
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    response_body = {
        "task": task.make_dict()}
    return make_response(jsonify(response_body), 200)
