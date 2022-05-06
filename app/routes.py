from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET"])
def get_books():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        is_complete = True
        if task.completed_at is None:
            is_complete = False
        tasks_response.append({"id": task.task_id, "title": task.title, "description": task.description, "is_complete": is_complete})
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods =["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    is_complete = True
    if task.completed_at is None:
        is_complete = False
    return {"task": {"id": task.task_id, "title": task.title, "description": task.description, "is_complete": is_complete}}

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"task {task_id} invalid, id must be integer"}, 400))
    
    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"task {task_id} not found"}, 404))

    return task
