from flask import Blueprint, make_response, request, jsonify, abort
from app.models.goal import Goal
from app import db
from flask import request
from datetime import datetime
# datetime.datetime.utcnow()

goal_bp = Blueprint("goal_bp", __name__, url_prefix = "/goals")


def validate_goal(id_):
    try:
        id_ = int(id_)
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    

    goal = Goal.query.get(id_)
    # gets the whole row in db with that particular id

    if not goal:
        abort(make_response({"message": f"Goal {id_} not found"}, 404))
        
    return goal

@goal_bp.route("", methods=["POST"])
def create_goal():

    request_body = request.get_json()

    try:
        new_goal = Goal.create(request_body)
   
    except KeyError:
        return abort(make_response({"details": "Invalid data"}, 400))

    
    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify(new_goal.to_dict()), 201)

@goal_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(
            {
                "id": goal.id,
                "title": goal.title
            }
        )

    return jsonify(goals_response), 200


@goal_bp.route("/<id>", methods=["GET"])
def get_one_goal(id):
    goal = validate_goal(id)

    return jsonify(goal.to_dict()), 200


@goal_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_goal(id)
    
    request_body = request.get_json()

    goal.update(request_body)

    db.session.commit()

    return jsonify(goal.to_dict()), 200


@goal_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = validate_goal(id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details": f"Goal {id} \"{goal.title}\" successfully deleted"}), 200)

