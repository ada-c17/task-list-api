from app import db
from flask import Blueprint, jsonify, make_response, request
from app.models.goal import Goal
from app.models.task import Task
from app.routes.request_helpers import handle_id_request, check_complete_request_body

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals_list = []

    goals = Goal.query.all()
    
    for goal in goals:
        goals_list.append(goal.make_response_dict())
    
    return make_response(jsonify(goals_list), 200)


@goals_bp.route("/<id>", methods=["GET"])
def get_goal_by_id(id):
    goal = handle_id_request(id, Goal)
    return make_response(jsonify({"goal": goal.make_response_dict()}), 200)


@goals_bp.route("", methods=["POST"])
def create_new_goal():
    request_body = check_complete_request_body(request, Goal)
    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    confirmation_msg = {"goal": new_goal.make_response_dict()}
    return make_response(jsonify(confirmation_msg), 201)

@goals_bp.route("/<id>", methods=["PUT"])
def update_goal_by_id(id):
    request_body = check_complete_request_body(request, Goal)
    active_goal = handle_id_request(id, Goal)

    active_goal.title = request_body["title"]

    db.session.commit()
    confirmation_msg = {"goal": active_goal.make_response_dict()}
    return make_response(jsonify(confirmation_msg), 200)

@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal_by_id(id):
    goal_to_delete = handle_id_request(id, Goal)

    db.session.delete(goal_to_delete)
    db.session.commit()

    confirmation_msg = {"details": f"Goal {id} \"{goal_to_delete.title}\" successfully deleted"}
    return make_response(jsonify(confirmation_msg), 200)

@goals_bp.route("/<id>/tasks", methods=["POST"])
def add_list_of_tasks_to_goal(id):
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
    active_goal = handle_id_request(id, Goal)
    response_body = active_goal.make_response_dict()

    task_list = []
    for task in active_goal.tasks:
        task_list.append(task.make_response_dict())

    response_body["tasks"] = task_list

    return make_response(jsonify(response_body), 200)