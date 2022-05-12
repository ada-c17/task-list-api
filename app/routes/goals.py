from flask import Blueprint, request, make_response, jsonify, abort
from app.models.goal import Goal
from app import db
from app.routes.helpers import valid_task, valid_goal, display_task, display_goal

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods = ["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        goal = Goal(title = request_body["title"])
    except:
        abort(make_response({"details":"Invalid data"}, 400))
        
    db.session.add(goal)
    db.session.commit()

    return make_response(
        jsonify({"goal":display_goal(goal)}), 201
    )

@goals_bp.route("", methods = ["GET"])
def get_goals():  
    goals = Goal.query.all()
    res = []
    for goal in goals:
        res.append(display_goal(goal))

    return make_response(jsonify(res), 200)
        

@goals_bp.route("/<goal_id>", methods = ["GET"])
def get_goal(goal_id):
    goal = valid_goal(goal_id)

    return make_response(
        jsonify({"goal":display_goal(goal)}), 200
    )

@goals_bp.route("/<goal_id>", methods = ["PUT"])
def update_goal(goal_id):
    goal = valid_goal(goal_id)
    request_body = request.get_json()
    try:
        goal.title = request_body["title"]
    except:
        abort(make_response({"details":"Invalid data"}, 400))

    db.session.commit()

    return make_response(
        jsonify({"goal":display_goal(goal)}), 200
    )

@goals_bp.route("/<goal_id>", methods = ["DELETE"])
def remove_goal(goal_id):
    goal = valid_goal(goal_id)
    db.session.delete(goal)
    db.session.commit()

    return make_response(
        jsonify({"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"}), 200
    )

@goals_bp.route("/<goal_id>/tasks", methods = ["POST"])
def add_task_to_goal(goal_id):
    goal = valid_goal(goal_id)
    request_body = request.get_json()
    for task_id in request_body["task_ids"]:
        task = valid_task(task_id)
        task.goal = goal
    db.session.commit()
            
    return jsonify({
        "id": goal.goal_id,
        "task_ids": [task.task_id for task in goal.tasks]
    }), 200

@goals_bp.route("/<goal_id>/tasks", methods = ["GET"])       
def get_all_tasks(goal_id):
    goal = valid_goal(goal_id)
    tasks = []
    for task in goal.tasks:
        task_str = display_task(task)
        task_str["goal_id"] = goal.goal_id
        tasks.append(task_str)

    return jsonify({
        "id":goal.goal_id,
        "title":goal.title,
        "tasks": tasks
    })
