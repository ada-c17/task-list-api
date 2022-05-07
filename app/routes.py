from app import db
from app.models.task import Task 
from datetime import datetime 
from flask import Blueprint, jsonify, abort, make_response, request

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except: 
        abort(make_response({"message": f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task: 
        abort(make_response({"message":f"task {task_id} not found"}, 404))
    
    return task 

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "completed_at" not in request_body: 
        try:
            new_task = Task(title=request_body["title"], 
                        description=request_body["description"])
        except KeyError:
            return {
                "details": "Invalid data"
            }, 400
    else: 
        try:
            new_task = Task(title=request_body["title"], 
                        description=request_body["description"],
                        completed_at=request_body["completed_at"])
        except KeyError:
            return {
                "details": "Invalid data"
            }, 400
    
    db.session.add(new_task)
    db.session.commit()

    response = {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": isinstance(new_task.completed_at, datetime)
    }

    return make_response(jsonify({"task": response}), 201)


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    query_params = request.args
    if 'sort' in query_params: 
        sort_order_query = request.args.get("sort")
        if sort_order_query == "asc":
            tasks = Task.query.order_by(Task.title.asc())
        elif sort_order_query == "desc":
            tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {
            "id": task.id, 
            "title": task.title,
            "description": task.description, 
            "is_complete": isinstance(task.completed_at, datetime)
            }
        )
    return make_response(jsonify(tasks_response))

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)
    task = Task.query.get(task_id)

    response = {
            "id": task.id, 
            "title": task.title,
            "description": task.description, 
            "is_complete": isinstance(task.completed_at, datetime)
    }

    return make_response(jsonify({"task": response}))

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    response = {
            "id": task.id, 
            "title": task.title,
            "description": task.description, 
            "is_complete": isinstance(task.completed_at, datetime)
    }

    return make_response(jsonify({"task": response}))

@tasks_bp.route("/<task_id>/<check_complete>", methods=["PATCH"])
def update_is_complete(task_id, check_complete=None): 
    task = validate_task(task_id)
    if check_complete == "mark_complete":
        task.completed_at = datetime.now()
    else:
        task.completed_at = None  
    
    db.session.commit()

    response = {
            "id": task.id, 
            "title": task.title,
            "description": task.description, 
            "is_complete": isinstance(task.completed_at, datetime)
    }

    return make_response(jsonify({"task": response}))


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()
    
    response = (f'Task {task.id} "{task.title}" successfully deleted')

    return make_response(jsonify({"details": response})) 


