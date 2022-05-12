from flask import Blueprint, jsonify, make_response, abort, request
from app.models.goal import Goal
from app import db
# helper function file import


goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")


'''
POST ROUTE
'''

# CREATE GOAL
@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return make_response(jsonify({"details": "Invalid data"}), 400)

    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    goal_response_body = {
            "id":  new_goal.goal_id,
            "title": new_goal.title
    }
    return make_response(jsonify({"goal": goal_response_body}), 201)


'''
GET ROUTES
# '''

# GET SAVED GOALS - ALL, QUERY PARAMS
@goal_bp.route("", methods=["GET"])
def read_saved_goals():

    goals = Goal.query.all()
    goals_response = []

    for goal_dict in goals:
        goals_response.append(
            {
                "id": goal_dict.goal_id,
                "title": goal_dict.title,
            }
        )
    return jsonify(goals_response)


def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"details":f"goal {goal_id} invalid"}, 400))

    goal = Goal.query.get(goal_id)
    if not goal:
        return abort(make_response({"details": f"Goal {goal_id} not found"}, 404))

    return goal


# GET ONE GOAL
@goal_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_goal(goal_id)

    return make_response(jsonify(goal.to_json()), 200)


'''
PUT ROUTE
'''

# UPDATE ONE GOAL
@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    goals_response_body = {
            "id": goal.goal_id,
            "title": goal.title,
    }

    return make_response(jsonify({"goal": goals_response_body}), 200)


'''
DELETE ROUTE
'''

# DELETE ONE GOAL
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    delete_response = f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"

    return make_response(jsonify({"details": delete_response}), 200)
