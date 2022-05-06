from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# create a new task
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"], description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    response_body = {"task": new_task.to_dict()}

    return make_response(jsonify(response_body), 201)

# retrieve all tasks
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks_response = []
    tasks = Task.query.all()

    for task in tasks:
        tasks_response.append(task.to_dict())
    
    return jsonify(tasks_response)

# retrieve one task by id
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task_by_id(task_id):
    pass

# check for valid task using id
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"Task #{task_id} invalid"}, 400))
    
    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"Task #{task_id} not found"}, 404))
    
    return task
