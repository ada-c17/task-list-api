from datetime import datetime
from typing import OrderedDict
from urllib.request import OpenerDirector
from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.goal import Goal

### Create a Goal:
goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@goal_bp.route("", methods = ["POST"])
def create_goals():
    request_body = request.get_json()
    if "title" in request_body:
        new_goal = Goal( 
            title = request_body["title"]
            )
    else:
        return jsonify({"details":"Invalid data"}), 400
        

    db.session.add(new_goal)
    db.session.commit()
    goal_response = {"goal": new_goal.to_dictionary()}
    return (jsonify(goal_response), 201)


### Get Goals
@goal_bp.route("", methods = ["GET"])
def get_goals():
    sort = request.args.get("sort")
    #Sort by assending (is default?)
    if sort == "asc":
        goals =Goal.query.order_by(Goal.title)
    #Sort by decending
    elif sort == "desc":
        goals =Goal.query.order_by(Goal.title.desc())
    #No Sort
    else:
        goals = Goal.query.all()
    
    goals_response = []
    for goal in goals: 
        goals_response.append(goal.to_dictionary())
        # If No Saved Goals wil stil return 200
    return (jsonify(goals_response), 200)


### Get One Goal: One Saved Goal
@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    goal_response = {"goal": goal.to_dictionary()}
    return (jsonify(goal_response), 200)

### Update Goal
@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]
    
    db.session.commit()

    goal_response = {"goal": goal.to_dictionary()}
    return (jsonify(goal_response), 200)

# Goal Complete
@goal_bp.route("/<goal_id>/mark_complete", methods=["PATCH"])
def goal_complete(goal_id):
    goal = validate_goal(goal_id)
    goal.completed_at = datetime.utcnow()
    
    db.session.commit()
    goal_response = {"goal": goal.to_dictionary()}
    return (jsonify(goal_response), 200)

# Goal Incomplete
@goal_bp.route("/<goal_id>/mark_incomplete", methods=["PATCH"])
def goal_incomplete(goal_id):
    goal = validate_goal(goal_id)
    goal.completed_at = None
    db.session.commit()
    goal_response = {"goal": goal.to_dictionary()}
    return (jsonify(goal_response), 200)


# Delete Goal: Deleting a Goal
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    response = {"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}
    return (jsonify(response), 200)


# Validate there are no matching Goal: Get, Update, and Delete

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message": f"Goal {goal_id} is invalid"}, 400))


    goal = Goal.query.get(goal_id)
    
    if not goal:
        abort(make_response({"message": f"Goal {goal_id} not found"}, 404))
    return goal


