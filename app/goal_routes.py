from webbrowser import Galeon
from attr import validate
from flask import Blueprint, request, make_response, jsonify, abort
from app import db
from app.models.goal import Goal

def validate_goal_id(goal_id):
    try: 
        goal_id = int(goal_id)
    except ValueError:
        abort(make_response({"msg":f"The goal with id {goal_id} is not found"}, 400))

    goal = Goal.query.get(goal_id)
    if goal: 
        return goal

    abort(make_response({"msg":f"The goal with id {goal_id} is not found"}, 404))

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")
# POST new task
@goals_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    # if "title" not in request_body:
    #     return make_response({"details": "Invalid data"}), 400

    new_goal = Goal(
        title=request_body["title"]
        )

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({'goal':
    {'id':new_goal.goal_id, 
    'title':new_goal.title}
    }), 201

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals_response = []
    goals = Goal.query.all()

    for goal in goals:
        goals_response.append({
            "id":goal.goal_id, 
            "title":goal.title
        })

    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal_id(goal_id)

    return jsonify({"goal":{
        "id":goal.goal_id, 
        "title":goal.title}
        })

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_task(goal_id):
    goal = validate_goal_id(goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit() 

    return jsonify({"goal": {
        "id":goal.goal_id, 
        "title":goal.title}
        })

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal_id(goal_id)
    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f'Goal {goal_id} \"{goal.title}\" successfully deleted'})
