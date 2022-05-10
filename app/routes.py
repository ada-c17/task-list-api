from flask import Blueprint, request, make_response, abort, jsonify
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# VALIDATE ID
def validate_id(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response(jsonify(f"Task {task_id} is invalid"), 400))
    task = Task.query.get(task_id)
    if not task:
        abort(make_response(jsonify(f"Task {task_id} not found"), 404))
    return task

# VALIDATE REQUEST
def validate_request(request):
    request_body = request.get_json()
    try:
        request_body["title"]
        request_body["description"]
    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400)) 
    return request_body

# POST /tasks
@tasks_bp.route("", methods=["POST"])
def create_new_task():
    request_body = validate_request(request)
    new_task = Task(
        title=request_body["title"],
        description=request_body["description"]
    )
    db.session.add(new_task)
    db.session.commit()
    return make_response({"task": new_task.to_dict()}, 201)

# GET /tasks
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    # Pull query parameters from url
    title_param = request.args.get("title")
    description_param = request.args.get("description")
    is_complete_param = request.args.get("is_complete")
    # start the query
    tasks = Task.query
    # build up the search criteria based on params present
    if title_param:
        tasks = tasks.filter_by(title=title_param)
    if description_param:
        tasks = tasks.filter_by(description=description_param)
    if is_complete_param:
        tasks = tasks.filter_by(completed_at=is_complete_param)
    # execute the search and return all records that meet the criteria built
    tasks = tasks.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response)

# GET /<task_id>
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_id(task_id)
    return {"task": task.to_dict()}

# PUT /<task_id>
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_id(task_id)
    request_body = validate_request(request)
    task.title = request_body["title"]
    task.description = request_body["description"]
    # task.completed_at = request_body["is_complete"]
    db.session.commit()
    return make_response(jsonify({"task": task.to_dict()}))

# DELETE /<task_id>
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_id(task_id)
    db.session.delete(task)
    db.session.commit()
    return make_response({"details": f'Task {task_id} "{task.title}" successfully deleted'})