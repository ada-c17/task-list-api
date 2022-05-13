from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
from .route_helpers import fetch_type

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

####################
#POST creates a goal
#route
#json: title
#returns created goal info
####################
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

####################
#GET gets all goals
#route
#returns a list of all goals
####################
@goal_bp.route("", methods=["GET"])
def fetch_all_goal():

    goals = Goal.query.all()

    goal_response = [goal.to_json() for goal in goals]
    return make_response(jsonify(goal_response),200)

####################
#GET gets a goal
#route /<goal_id>
#returns the goal info
####################
@goal_bp.route("/<goal_id>", methods=["GET"])
def fetch_a_goal(goal_id):
    goal = fetch_type("goal", goal_id)
    return make_response(jsonify({"goal": goal.to_json()}), 200)

####################
#PUT updates goal
#route /<goal_id>
#json: title
#returns updates goal info
####################
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

####################
#DELETE deletes a goal
#route /<goal_id>
#returns message confirming deleted goal
####################
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_a_goal(goal_id):
    goal = fetch_type("goal", goal_id)
    db.session.delete(goal)
    db.session.commit()
    return make_response(jsonify({"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}), 200)

#######################################################
####################
#POST adds tasks as children of goal
#route /<goal_id>/tasks
#json: task_ids(list of task_ids to become children) 
#returns goal_id, task_ids(list of task ids)
####################
@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    request_body = request.get_json()
    try:
        for task_id in request_body["task_ids"]:
            task = fetch_type("task", task_id)
            task.goal_id = goal_id 
    except:
        abort(make_response(jsonify({"details":f"Invalid data"}), 400))

    db.session.commit()
    return make_response(jsonify({"id": int(goal_id), "task_ids": request_body["task_ids"]}), 200)

####################
#GET shows all task in a goal
#route /<goal_id>/tasks
#returns dictionary of goal info with a tasks key containing a dict with all task infos
####################
@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_all_tasks_for_goal(goal_id):
    goal = fetch_type("goal", goal_id)
    response_tasks = [task.to_json() for task in goal.tasks]
    response_message = goal.to_json() #there is room to refactor this json build if I have time
    response_message["tasks"] = response_tasks
    return make_response(jsonify(response_message),200)
