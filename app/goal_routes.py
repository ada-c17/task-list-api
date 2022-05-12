from flask import Blueprint, jsonify, make_response, request, abort
from app.models.goal import Goal
from app.models.task import Task
from .routes import validate_task
from app import db

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

#view all goals
@goals_bp.route("", methods=["GET"])
def view_goals():
    title_query = request.args.get("sort")
    if title_query == "asc":
        goals = Goal.query.order_by(Goal.title.asc()).all()
    elif title_query == "desc":
        goals = Goal.query.order_by(Goal.title.desc()).all()
    else:
        goals = Goal.query.all()
    goals_response = []

    for goal in goals:
        goals_response.append(goal.to_json())
        
    return jsonify(goals_response), 200


#view one goal
@goals_bp.route("/<int:id>", methods=["GET"])
def view_goal(id):
    goal = validate_goal(id)

    return jsonify({"goal": goal.to_json()}), 200


#create a goal
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal(title = request_body["title"])


    except KeyError:
        return make_response({"details": "Invalid data"},400)

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal":new_goal.to_json()}), 201


#delete a goal
@goals_bp.route("/<int:id>", methods=["DELETE"])
def delete_goal(id):
    goal = validate_goal(id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f'Goal {id} "{goal.to_json()["title"]}" successfully deleted'}), 200


#delete a goal
# @goals_bp.route("/delete", methods=["POST"])
# def delete_goal():
#     request_body = request.get_json()
#     try:
#         delete_goal = request_body["id"]
#         goal = validate_goal(delete_goal)

#     except KeyError:
#         return make_response({"details": "Invalid data"},400)

#     db.session.delete(goal)
#     db.session.commit()

#     return jsonify({"details": f'Goal {id} "{goal.to_json()["title"]}" successfully deleted'}), 200


#update a goal
@goals_bp.route("/<int:id>", methods=["PUT"])
def update_goal(id):
    goal = validate_goal(id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return jsonify({"goal":goal.to_json()}), 200


@goals_bp.route("/<int:id>/tasks", methods=["GET"])
def view_goal_tasks(id):
    goal = validate_goal(id)
    goal_tasks = [Task.to_json(task) for task in goal.tasks]
    return jsonify({"id": goal.id, "title": goal.title, "tasks": goal_tasks}), 200


@goals_bp.route("/<int:id>/tasks", methods=["POST"])
def add_tasks_to_goal(id):
    goal = validate_goal(id)

    request_body = request.get_json()

    task_list = []
    for id in request_body["task_ids"]:
        task = validate_task(id)
        task_list.append(task)

    for task in task_list:
        if task not in goal.tasks:
            goal.tasks.append(task)

    db.session.commit()
    return jsonify({"id": goal.id, "task_ids": request_body["task_ids"]}), 200


def validate_goal(id):
    try:
        id = int(id)
    except:
        return abort(make_response({"message": f"Goal {id} is invalid"}, 400))

    goal = Goal.query.get(id)

    if not goal:
        return abort(make_response({"message": f"Goal {id} not found"}, 404))
    
    return goal