from app import db
from app.models.task import Task 
from flask import Blueprint, abort, jsonify, make_response, request  

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return {
        "details": "Invalid data"
    }, 400
        #return make_response("Invalid Request", 400)

    new_task = Task(title=request_body["title"],
                    description=request_body["description"]
                    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": new_task.is_complete
            }
            }), 201


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    title_query = request.args.get("title")

    if title_query is not None:
        tasks = Task.query.filter_by(title=title_query)
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        })
    return jsonify(tasks_response)


##### helper function #####
def validate_task(id_of_task):
    try:
        id_of_task = int(id_of_task)
    except:
        abort(make_response({"message":f"task {id_of_task} invalid"}, 400))

    task = Task.query.get(id_of_task)

    if not task:
        abort(make_response({"message":f"task {id_of_task} not found"}, 404))

    return task
##### helper function #####


@tasks_bp.route("/<id_of_task>", methods=["GET"])
def read_one_task(id_of_task):
    task = validate_task(id_of_task)
    return jsonify({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
            }
            })


@tasks_bp.route("/<id_of_task>", methods=["PUT"])
def update_task(id_of_task):
    task = validate_task(id_of_task)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return jsonify({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
            }
            })


@tasks_bp.route("/<id_of_task>", methods=["DELETE"])
def delete_task(id_of_task):
    task = validate_task(id_of_task)

    db.session.delete(task)
    db.session.commit()

    return {
        "details": f'Task 1 "{task.title}" successfully deleted'
    }
    #"details": "Task 1 \"Go on my daily walk 🏞\" successfully deleted"