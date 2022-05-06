from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        is_complete = check_is_complete(task)
        tasks_response.append({"id": task.task_id, "title": task.title, "description": task.description, "is_complete": is_complete})
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods =["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    is_complete = check_is_complete(task)
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

def check_is_complete(task):
    '''Takes in one instance of task object, returns the value that should be assigned to is_complete for that object'''
    if task.completed_at is None:
        return False
    return True

@tasks_bp.route("", methods=["POST"])
def handle_tasks():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()
    
    is_complete = check_is_complete(new_task)

    body = {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title ,
            "description": new_task.description,
            "is_complete": is_complete
        }
    }

    return make_response(jsonify(body), 201)