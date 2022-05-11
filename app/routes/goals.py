from xml.dom.minidom import Identified
from urllib3 import connection_from_url
from app import db
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import date
from app.models.goal import Goal
from app.models.task import Task

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def handle_id_request(id):
    try:
        id = int(id)
    except:
        abort(make_response({"msg": f"Invalid Goal ID '{id}'."}, 400))

    goal = Goal.query.get(id)

    if not goal:
        abort(make_response({"msg": f"Goal ID '{id}' does not exist."}, 404))

    return goal

def check_complete_request_body(request):
    request_body = request.get_json()
    if all(element in request_body for element in Goal.expected_elements):
        if all(type(request_body[element]) == Goal.expected_elements[element] \
                    for element in Goal.expected_elements):
                        return request_body
    abort(make_response({"details": "Invalid data"}, 400))

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals_list = []

    goals = Goal.query.all()
    
    for goal in goals:
        goals_list.append(goal.make_response_dict())
    
    return make_response(jsonify(goals_list), 200)



@goals_bp.route("/<id>", methods=["GET"])
def get_goal_by_id(id):
    goal = handle_id_request(id)
    return make_response(jsonify({"goal": goal.make_response_dict()}), 200)


@goals_bp.route("", methods=["POST"])
def create_new_goal():
    request_body = check_complete_request_body(request)
    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    confirmation_msg = {"goal": new_goal.make_response_dict()}
    return make_response(jsonify(confirmation_msg), 201)

@goals_bp.route("/<id>", methods=["PUT"])
def update_goal_by_id(id):
    request_body = check_complete_request_body(request)
    active_goal = handle_id_request(id)

    active_goal.title = request_body["title"]

    db.session.commit()
    confirmation_msg = {"goal": active_goal.make_response_dict()}
    return make_response(jsonify(confirmation_msg), 200)

@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal_by_id(id):
    goal_to_delete = handle_id_request(id)

    db.session.delete(goal_to_delete)
    db.session.commit()

    confirmation_msg = {"details": f"Goal {id} \"{goal_to_delete.title}\" successfully deleted"}
    return make_response(jsonify(confirmation_msg), 200)

@goals_bp.route("/<id>/tasks", methods=["POST"])
def add_list_of_tasks_to_goal(id):
    #request_body = check_complete_request_body(request)
    task_ids = request.get_json()["task_ids"]
    id = int(id)
    for task in task_ids:
        active_task = Task.query.get(task)
        active_task.goal_id = id

    db.session.commit()

    confirmation_msg = {"id": id, "task_ids": task_ids}
    return make_response(jsonify(confirmation_msg), 200)

@goals_bp.route("/<id>/tasks", methods=["GET"])
def get_task_list_by_goal_id(id):
    #request_body = check_complete_request_body(request)
    active_goal = handle_id_request(id)
    response_body = active_goal.make_response_dict()
    
    task_list = []
    for task in active_goal.tasks:
        task_list.append(task.make_response_dict())

    response_body["tasks"] = task_list

    return make_response(jsonify(response_body), 200)