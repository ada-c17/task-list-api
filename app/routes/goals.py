from flask import Blueprint, jsonify, abort, make_response, request
from app.models.goal import Goal
from app import db

goals_bp = Blueprint("goals_bp", __name__,  url_prefix="/goals")

def validate_goal(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"goal {id} invalid"}, 400))
    goal = Goal.query.get(id)
    if not goal:
        abort(make_response({"message":f"goal {id} not found"}, 404))
    return goal


@goals_bp.route("", methods=["GET"])
def read_all_goals():
    params = request.args   
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(
            {
                "id": goal.goal_id,
                "title": goal.title,
            }
        )
    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_goal(goal_id)
    return  goal.to_json()    

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(title=request_body["title"])
    except KeyError:
        return {"details": "Invalid data"}, 400
    db.session.add(new_goal)
    db.session.commit()
    return new_goal.to_json(), 201    


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit()
    return goal.to_json()

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)
    db.session.delete(goal)
    db.session.commit()

    return {"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}    

@goals_bp.errorhandler(404)
def pageNotFound(error):
    return "<h1> Page not found </h1>", 404      