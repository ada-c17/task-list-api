from flask import Blueprint, make_response, request,jsonify, abort
from app import db
from app.models.goal import Goal

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message":f"Goal {goal_id} invalid"}, 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message":f"Goal {goal_id} not found"}, 404))

    return goal

@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    new_goal = Goal(title = request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    response_body = {"goal":
        {
            "id": new_goal.goal_id,
        "title": new_goal.title
        }
    }
    return jsonify(response_body), 201

@goal_bp.route("", methods=["GET"])
def get_all_saved_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(
            {
                "id": goal.goal_id,
                "title": goal.title,
            }
        )
    return jsonify(goals_response), 200

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)

    return jsonify({"goal":
    {"id": goal.goal_id,
    "title": goal.title}
    }) 

@goal_bp.route("/<goalid>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()
    
    response_body = {"goal":
        {"id": goal.goal_id,
        "title": goal.title}
        }
    return jsonify(response_body), 200