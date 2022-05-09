import json
from urllib import response
from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods = ["POST"])
def manage_post_tasks():
    request_body = request.get_json()
    new_task = Task(
        title = request_body["title"],
        description = request_body["description"]
        # completed_at = request_body["completed_at"]
        )

    db.session.add(new_task)
    db.session.commit()

    response_body = dict()
    response_body["task"] = new_task.to_dictionary()

    return make_response(jsonify(response_body), 201)

@tasks_bp.route("", methods=["GET"])
def manage_get_tasks():
    tasks = Task.query.all()
    # title_query = request.args.get("title")
    # is_complete = request.args.get("completed_at")

    # if title_query:
    #     tasks = Task.query.filer_by(title=title_query)
    # else:
    #     tasks = Task.query.filter_by(title=title_query)

    # if Task.completed_at == None:
    # change the key of completed_at to "is complete"
    # change value None == False
    # for task in tasks:
    #     if Task.completed_at == None:
    #         task["completed_at"] == task["is_complete"]
    #         task["is_complete"] == False
    #     else:
    #         Task.completed_at == is_complete
    #         task["completed_at"] == task["is_complete"]
    tasks_response = [task.to_dictionary() for task in tasks]
    # print(tasks_response)
    return jsonify(tasks_response)


@tasks_bp.route("/<id>", methods=["GET"])
def get_task_by_id(id):
    task = get_task(id)
    response_body = dict()
    response_body["task"] = task.to_dictionary()

    return jsonify(response_body)

@tasks_bp.route("/<id>", methods=["PUT"])
def update_task_by_id(id):
    task = get_task(id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return get_task_by_id(id)




def get_task(id):
    try:
        task_id = int(id)
    except ValueError:
        abort(make_response(jsonify({"message": f"task {id} invalid"}), 400))
    
    task = Task.query.get(task_id)

    if not task:
        abort(make_response(jsonify({"message": f"task {id} not found"}), 404))
    else: 
        return task