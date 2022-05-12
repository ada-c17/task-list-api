from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.goal import Goal
from datetime import datetime
from app.routes.tasks import validate_task

goals_bp = Blueprint("goals", __name__, url_prefix='/goals')

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        abort(make_response({"msg": f"Invalid Id: '{goal_id}'. ID must be an integer"}, 400))

    chosen_goal = Goal.query.get(goal_id)

    if not chosen_goal:
        abort(make_response({"msg": f"Goal {goal_id} not found"}, 404))

    return chosen_goal

@goals_bp.route("", methods=["GET", "POST"])
def handle_goals():
    if request.method == "GET":
        goals = Goal.query.all()
        goals_response = []
        for goal in goals:
            goals_response.append(goal.to_dict())
        return jsonify(goals_response)

    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body:
            return jsonify({"details": "Invalid data"}), 400

        new_goal = Goal(title=request_body["title"])
        db.session.add(new_goal)
        db.session.commit()
        return jsonify({
            "goal" : new_goal.to_dict()
        }), 201

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    chosen_goal = validate_goal(goal_id)
    return jsonify({
        "goal": chosen_goal.to_dict()
    })

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    request_body = request.get_json()
    chosen_goal = validate_goal(goal_id)

    if "title" not in request_body:
        return jsonify({"details": "Invalid data"}), 400
    
    chosen_goal.title = request_body["title"]

    db.session.commit()

    return jsonify({
        "goal": chosen_goal.to_dict()
    })

    
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    chosen_goal = validate_goal(goal_id)

    db.session.delete(chosen_goal)
    db.session.commit()

    return jsonify({"details": f'Goal {goal_id} "{chosen_goal.title}" successfully deleted'})


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    chosen_goal = validate_goal(goal_id)

    request_body = request.get_json()

    if "task_ids" not in request_body:
        return jsonify({
            "details": "Invalid data"
            }), 400

    tasks = []
    for task_id in request_body["task_ids"]:
        tasks.append(validate_task(task_id))
    for task in tasks:
        task.goal = chosen_goal

    db.session.commit()

    return jsonify({
        "id": chosen_goal.id,
        "task_ids": request_body["task_ids"]
    })



@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_one_goal(goal_id):
    chosen_goal = validate_goal(goal_id)

    tasks_list = []
    for task in chosen_goal.tasks:
        tasks_list.append(task.to_dict())
    

    return jsonify({
        "id": chosen_goal.id,
        "title": chosen_goal.title,
        "tasks": tasks_list
    })


