from flask import Blueprint, make_response, request, jsonify, abort
from app.models.task import Task
from app import db
from flask import request
from datetime import datetime
# datetime.datetime.utcnow()

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")


def validate_task(id_):
    try:
        id_ = int(id_)
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    

    task = Task.query.get(id_)
    # gets the whole row in db with that particular id

    if not task:
        abort(make_response({"message": f"Task {id_} not found"}, 404))
        
    return task


@tasks_bp.route("", methods=["POST"])
def create_task():
   
    request_body = request.get_json()
    try:
        new_task = Task.create(request_body)
    # new_task = Task(title=request_body["title"],
    #                 description=request_body["description"])
    except KeyError:
        return abort(make_response({"details": "Invalid data"}, 400))

    
    db.session.add(new_task)
    db.session.commit()

    # return make_response(jsonify(f"Task {new_task.title} successfully created"), 201)
    return make_response(jsonify({"task": new_task.to_json()}), 201)


@tasks_bp.route("/<tasks_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(tasks_id):
    task = validate_task(tasks_id)
    
    # request_body = request.get_json()
    # task.completed_at = request_body["completed_at"]
    task.completed_at = datetime.utcnow()
    
    # request_body = request.get_json()
    # task.completed_at = response_body["completed_at"]
    # task.update(response_body)

    db.session.commit()

    return make_response(jsonify({"task": task.to_json()}), 200)

@tasks_bp.route("/<tasks_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(tasks_id):
    task = validate_task(tasks_id)
   
    task.completed_at = None

    # request_body = request.get_json()
    # task.completed_at = response_body["completed_at"]
    # task.update(response_body)

    db.session.commit()

    return make_response(jsonify({"task": task.to_json()}), 200)


@tasks_bp.route("", methods=["GET"])
def get_tasks():
    title_param = request.args.get("title")

    sort_param = request.args.get("sort")

    if title_param:
        tasks = Task.query.filter_by(title=title_param)
    else:
        if sort_param == "desc":
            tasks = Task.query.order_by(Task.title.desc()).all()
        else:
        # tasks = Task.query.all()
            tasks = Task.query.order_by(Task.title.asc()).all()
    

    task_response_body = []
    for task in tasks:
        task_response_body.append(task.to_json())

    # [task.tojson() for task in tasks]     

    return jsonify(task_response_body), 200



@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)

    return jsonify({"task": task.to_json()}), 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_planet(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.update(request_body)

    db.session.commit()

    return make_response(jsonify({"task": task.to_json()}), 200)

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f"Task {task_id} \"{task.title}\" successfully deleted"}), 200)

