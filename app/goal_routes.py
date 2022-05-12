from app import db
from app.models.goal import Goal
from app.models.task import Task 
from flask import Blueprint, request, jsonify, make_response, abort
from datetime import datetime
import requests, json
import os
from dotenv import load_dotenv

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# CREATE aka POST new goal at endpoint: /goals
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response(jsonify(dict(details="Invalid data")), 400)
    
    new_goal = Goal.create(request_body)
    # new_goal = Goal(title=request_body["title"],)
    
    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": new_goal.to_dict()}), 201)   

    # GET ALL goalS aka READ at endpoint /goals
@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals_response = []

    title_query = request.args.get("sort")

    if title_query == "asc":
        goals = Goal.query.order_by(Goal.title.asc())

    elif title_query == "desc":
        goals = Goal.query.order_by(Goal.title.desc())
    
    else:
        goals = Goal.query.all()

    goals_response = [goal.to_dict() for goal in goals]

    return make_response(jsonify(goals_response), 200) 

#####
# GET aka READ goal at endpoint: /goals/id 
@goals_bp.route("/<id>", methods=["GET"])
def get_goal_by_id(id):
    goal = validate_goal(id)

    # NOTE: Flask will automatically convert a dictionary into an HTTP response body. 
    # If we don't want to remember this exception, we can call jsonify() with the dictionary as an argument to return the result
    return jsonify({"goal": goal.to_dict()}), 200
    # return make_response(jsonify({"goal": goal.to_dict()}), 201)

# *************Could alternatively use a hash to look things up by id.  ...need to practice this later. 

@goals_bp.route("/<id>", methods=['PUT'])
def update_goal(id):
    goal = validate_goal(id)

    request_body = request.get_json()

    goal.update(request_body)
    db.session.commit()
    return jsonify({"goal": goal.to_dict()}), 200
    
# DELETE /goals/id
@goals_bp.route("<id>", methods=['DELETE'])
def delete_one_goal(id):
    goal = validate_goal(id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({'details': f'Goal {id} "{goal.title}" successfully deleted'}), 200

#QUALITY CONTROL HELPER FUNCTION
def validate_goal(id):
    try:
        id = int(id)
    except ValueError: 
        # return jsonify({}), 400     .....OR
        abort(make_response(jsonify(dict(details=f"invalid id: {id}")), 400))

    goal = Goal.query.get(id)
    if goal:
        return goal

    elif not goal:
        abort(make_response(jsonify(dict(message= f"goal {id} not found")), 404))

    
#########   
# PATCH a goal at endpoint: goals/id  #Remember PATCH is just altering one or some attributes whereas PUT replaces a record. 
@goals_bp.route("/<id>", methods=["PATCH"])
def update_one_goal(id):
    goal = validate_goal(id)
    request_body = request.get_json()
    goal_keys = request_body.keys()

    if "title" in goal_keys:
        goal.title = request_body["title"]

    db.session.commit()
    return make_response(f"Goal# {goal.goal_id} successfully updated"), 200

# PATCH a goal at endpoint: goals/id/mark_complete 
@goals_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_complete(id):
    goal = validate_goal(id)
    
    # if goal.completed_at:
    goal.completed_at = datetime.utcnow()

    db.session.commit()

    return make_response(jsonify({"goal": goal.to_dict()}), 200)

# PATCH a goal at endpoint: goals/id/mark_incomplete
@goals_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(id):
    goal = validate_goal(id)

    goal.completed_at = None

    db.session.commit()
    return make_response(jsonify({"goal": goal.to_dict()}), 200)





