# import the necessary modules
from app import db
from app.models.task import Task
# import dependencies
from flask import Blueprint, jsonify, make_response, request, abort

# initialize Blueprint instance
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"Task ID {task_id} is invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"Task ID {task_id} not found"}, 404))

    return task

@tasks_bp.route("", methods = ["POST"])
def add_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400

    new_task = Task(title = request_body["title"],
                    description = request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    rsp = {
        "id":new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": False
        }
    
    return make_response({"task":rsp}, 201)

# As a client, I want to be able to make a GET request to /tasks when there are zero saved tasks
@tasks_bp.route("", methods = ["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {
                "id":task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            }
        )
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    return make_response({"task":{"id":task.id,
                                "title": task.title,
                                "description": task.description,
                                "is_complete": False
                                }}, 200)

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response({"task":{"id":task.id,
                                "title": task.title,
                                "description": task.description,
                                "is_complete": False
                                }}, 200)

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details":f"Task {task.id} \"{task.title}\" successfully deleted"})
