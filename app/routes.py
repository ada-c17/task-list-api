import json
from urllib import response
from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy import desc
from app import db
from app.models.task import Task


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods = ["POST"])
def manage_post_tasks():
    request_body = request.get_json()
    title = request_body.get("title")
    description = request_body.get("description")
    # print(title)
    # print(description)
    # print(request_body)
    if title is None or description is None:
        response_body = make_response(jsonify({"details": "Invalid data"}), 400)
        # print("inside if statement")
        # print(response_body)
        return response_body
        
    new_task = Task(
        title = request_body.get("title"),
        description = request_body.get("description")
        # completed_at = request_body["completed_at"]
        )

    db.session.add(new_task)
    db.session.commit()

    response_body = dict()
    response_body["task"] = new_task.to_dictionary()

    return make_response(jsonify(response_body), 201)


@tasks_bp.route("", methods=["GET"])
def manage_get_tasks():
    sort_param = request.args.get("sort")
    # print(sort_param)
    # asc or desc

    # order ascending:
    # need request to have asc
    # tasks_asc = Task.query.order_by(Task.title).all()
    # order descending:
    # need req to have desc
    # tasks_desc = Task.query.order_by(desc(Task.title)).all()
    
    if sort_param == "asc":
        tasks = Task.query.order_by(Task.title).all()
    elif sort_param == "desc":
        tasks = Task.query.order_by(desc(Task.title)).all()
    else:
        tasks = Task.query.all()

    ### this might query titles and need a change in task_response
    #   title_query = request.args.get("title")
    ### this might be an alternative
    # tasks = Task.query.all()
    
    # if title_query:
    #     tasks = Task.query.order_by(Task.title).all()
    # else:
    #     tasks = Task.query.all()

    tasks_response = [task.to_dictionary() for task in tasks]
    # print(tasks_response)

    return jsonify(tasks_response)

def sort_task_by_title(title):
    pass


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


@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task_by_id(id):
    task = get_task(id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f"Task {task.id} \"{task.title}\" successfully deleted"}), 200)


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