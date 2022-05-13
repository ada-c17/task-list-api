import json
import os
import datetime
from pandas import json_normalize
import requests
from urllib import response
from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy import desc
from app import db
from app.models.goal import Goal
from app.models.task import Task
from .helper_routes import get_record_by_id


goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

##CRUD
##CREATE : POST
@goals_bp.route("", methods=["POST"])
def manage_post_goals():
    request_body = request.get_json()
    title = request_body.get("title")

    if title is None:
        response_body = make_response(jsonify({"details": "Invalid data"}), 400)
        return response_body
    

    goals = Goal.from_dict(request_body)


    db.session.add(goals)
    db.session.commit()

    return jsonify({"goal":goals.to_dictionary()}), 201

#READ : GET
@goals_bp.route("", methods=["GET"])
def manage_get_goals():
    goals = Goal.query.all()
    goal_dictionary = [goal.to_dictionary() for goal in goals]

    return jsonify(goal_dictionary)



@goals_bp.route("/<id>", methods=["GET"])
def get_goal_by_id(id):
    goal = get_goal(id)
    # response_body = dict()
    # response_body = goal.to_dictionary()
    return jsonify({"goal":goal.to_dictionary()})


#UPDATE : PUT
@goals_bp.route("/<id>", methods=["PUT"])
def update_goal_by_id(id):
    goal = get_goal(id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return get_goal_by_id(id)


#DELETE : DELETE
@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal_by_id(id):
    goal = get_goal(id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details": f"Goal {goal.id} \"{goal.title}\" successfully deleted"}), 200)



# #### FRIENDSHIP ROUTEs
# @goals_bp.route("/<id>/tasks", methods=["POST"])
# def post_tasks_for_goal(id):
#     goal = get_goal(id)

#     request_body = request.get_json()
#     task_id = request_body["task_ids"]
#     new_task = Task(
#         title=request_body["title"],
#         description=request_body["description"],
#         completed_at=request_body["completed_at"]
#         )
#     print(new_task)
#     new_task.goal = goal

#     db.session.add(new_task)
#     db.session.commit()

#     return jsonify(new_task.to_dictionary()),201

# no request body
# response body returns {goal{tasks}}



## HELPER FUNCTIONS:
def get_goal(id):
    try:
        goal_id = int(id)
    except ValueError:
        abort(make_response(jsonify({"message": f"goal {id} invalid"}), 400))
    
    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response(jsonify({"message": f"goal {id} not found"}), 404))
    else: 
        return goal
