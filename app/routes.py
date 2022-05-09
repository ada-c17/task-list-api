from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"message":f"task {task_id} not found"}, 404))

    return task

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["GET", "POST"])
def handle_task():
    if request.method == "GET":
        tasks = Task.query.all()
        task_response = []
        for task in tasks:
            task_response.append({
                "id":task.task_id,
                "title":task.title,
                "description":task.description,
                "is_complete":False
            })
        return jsonify(task_response)

    elif request.method == "POST":
        request_body = request.get_json()

        try:
            new_task = Task(title=request_body["title"],
                        description=request_body["description"])
        except:
            abort(make_response({"details": "Invalid data"}, 400))

        db.session.add(new_task)
        db.session.commit()

        response_body = {
            "task": {
                "id": new_task.task_id,
                "title": new_task.title,
                "description": new_task.description,
                "is_complete": False
        }}

        return make_response(response_body, 201)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)

    return jsonify({
        "task":{
        "id":task.task_id,
        "title":task.title,
        "description":task.description,
        "is_complete":False
    }})


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    response_body = {
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
        }}

    return make_response(response_body)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    response_body = {
        "details": f'Task {task.task_id} "{task.title}" successfully deleted'
    }

    return make_response(response_body)
