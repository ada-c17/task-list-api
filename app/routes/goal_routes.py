from datetime import datetime
from email import message
from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.goal import Goal
from sqlalchemy import asc, desc
import os
import requests

goal_bp = Blueprint('goals', __name__, url_prefix='/goals')

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        abort(make_response(jsonify({'details': 'Invalid data'}), 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        return abort(make_response(jsonify(f"Goal {goal_id} not found"), 404))
    
    return goal


@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    try:
        # completed = request_body.get("completed_at")
        # if completed:
        #     new_goal = Goal(
        #         title = request_body["title"],
        #         description = request_body["description"],
        #         completed_at = request_body["completed_at"]
        #     )
        # else:
        new_goal = Goal(
            title = request_body["title"]
        )

        db.session.add(new_goal)
    except KeyError:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))

    db.session.commit()
    
    # goal = Goal.query.get(int(new_goal.goal_id))
    # is_complete = bool(goal.completed_at)

    return make_response({"goal": new_goal.to_dict()}, 201)
    # return make_response({"goal": goal.to_dict(is_complete)}, 201)

@goal_bp.route("", methods=["GET"])
def read_all_goals():
    # title_param = request.args.get("title")
    # description_param = request.args.get("description")
    # completed_param = request.args.get("mark_complete")
    sort_param = request.args.get("sort")

    goals = Goal.query

    # if title_param:
    #     goals = goals.filter_by(title=title_param)
    # if description_param:
    #     goals = goals.filter_by(description=description_param)
    # if completed_param:
    #     goals = goals.filter_by(mark_complete=completed_param)
    if sort_param:
        if sort_param == 'asc':
            goals = Goal.query.order_by(asc(Goal.title))
        else:
            goals = Goal.query.order_by(desc(Goal.title))
    
    goals = goals.all()

    goals_response = []
    for goal in goals:
        # is_complete = bool(goal.completed_at)

        # goals_response.append(goal.to_dict(is_complete))
        goals_response.append(goal.to_dict())

    return jsonify(goals_response)

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    # is_complete = bool(goal.completed_at)
    
    return {"goal": goal.to_dict()}
    # return {"goal": goal.to_dict(is_complete)}

@goal_bp.route("/<goal_id>", methods=["PUT"])
def replace_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]
    
    db.session.commit()

    return {"goal": goal.to_dict()}

@goal_bp.route("/<goal_id>/mark_complete", methods=["PATCH"])
def complete_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    
    # goal.completed_at = datetime.utcnow()
    # is_complete = bool(goal.completed_at)

    title = request_body.get("title")

    if title:
        goal.title = request_body["title"]
        # auth_token = os.environ.get("Authorization")
        # headers = {
        #     "Authorization": auth_token,
        #     "Content-Type": "application/json; charset=utf-8"
        #     }

        # data = {
        #     "channel": 'test-channel',
        #     "text": f"Someone just completed the goal {title}"
        # }

        # slack_response = requests.post("https://slack.com/api/chat.postMessage", headers=headers, json=data)

    db.session.commit()
    
    return {"goal": goal.to_dict()}
    # return {"goal": goal.to_dict(is_complete)}

@goal_bp.route("/<goal_id>/mark_incomplete", methods=["PATCH"])
def incomplete_goal(goal_id):
    goal = validate_goal(goal_id)
    
    goal.completed_at = None
    # is_complete = bool(goal.completed_at)

    db.session.commit()

    return {"goal": goal.to_dict()}
    # return {"goal": goal.to_dict(is_complete)}

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()
    
    return jsonify({'details': f'Goal "{goal.title}" successfully deleted'})