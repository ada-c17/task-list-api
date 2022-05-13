from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
from .route_helpers import fetch_type

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(title = request_body["title"])
        db.session.add(new_goal)
        db.session.commit()
    except:
        abort(make_response(jsonify({"details":f"Invalid data"}), 400))
    return make_response(jsonify({"goal": new_goal.to_json()}), 201)

@goal_bp.route("", methods=["GET"])
def fetch_all_goal():

    goals = Goal.query.all()

    goal_response = []
    for goal in goals:
        goal_response.append(goal.to_json())
    return make_response(jsonify(goal_response),200)

@goal_bp.route("/<goal_id>", methods=["GET"])
def fetch_a_goal(goal_id):
    goal = fetch_type("goal", goal_id)
    return make_response(jsonify({"goal": goal.to_json()}), 200)

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_a_goal(goal_id):
    
    goal = fetch_type("goal", goal_id)
    request_body = request.get_json()
    try:
        goal.title = request_body["title"]
        db.session.commit()
    except:
        abort(make_response(jsonify({"details":f"Invalid data"}), 400))
    return make_response(jsonify({"goal": goal.to_json()}),200)

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_a_goal(goal_id):
    goal = fetch_type("goal", goal_id)
    db.session.delete(goal)
    db.session.commit()
    return make_response(jsonify({"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}), 200)

    #######################################################
@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    request_body = request.get_json()
    # goal = fetch_type("goal", goal_id) #unsure if this works
    try:
        for task_id in request_body["task_ids"]:
            task = fetch_type("task", task_id)
            task.goal_id = goal_id 
            # task.goal = goal     
    except:
        abort(make_response(jsonify({"details":f"Invalid data"}), 400))

    db.session.commit()
    return make_response(jsonify({"id": int(goal_id), "task_ids": request_body["task_ids"]}), 200)
#     try:
#         new_goal = Goal(title = request_body["title"])
#         db.session.add(new_goal)
#         db.session.commit()
#     except:
#         abort(make_response(jsonify({"details":f"Invalid data"}), 400))
#     return make_response(jsonify({"goal": new_goal.to_json()}), 201)

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_all_tasks_for_goal(goal_id):
    goal = fetch_type("goal", goal_id)
    response_tasks = []
    for task in goal.tasks:
        response_tasks.append(task.to_json(True))
    response_message = goal.to_json()
    response_message["tasks"] = response_tasks
    return make_response(jsonify(response_message),200)
