from flask import Blueprint, jsonify, make_response, abort, request
from app.models.goal import Goal
from app.models.task import Task
from app import db

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

#Create goal
@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    try:
        title = request_body['title']
    except KeyError:
        return abort(make_response({"details": 'Invalid data'}, 400))

    new_goal = Goal(
        title = title, 
    )

    db.session.add(new_goal)
    db.session.commit()

    response = {
        "goal": new_goal.to_json()
    }

    return make_response(jsonify(response), 201)


#Get all goals or no saved goals
@goal_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_json())

    return make_response(jsonify(goals_response), 200)

#Get One Goal: One Saved Goal
@goal_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if not goal:
        return abort(make_response({"message": f"Goal {goal_id} is not found"}, 404))

    response = {
        "goal": goal.to_json()
    }

    return jsonify(response)

#Update one goal
@goal_bp.route("/<goal_id>", methods = ["PUT"])
def update_one_goals(goal_id):
    goal = Goal.query.get(goal_id)

    if not goal:
        return abort(make_response({"message": f"Goal {goal_id} is not found"}, 404))

    request_body = request.get_json()

    goal.title = request_body['title']

    db.session.commit()

    return make_response(jsonify({"goal": goal.to_json()}), 200)

#Delete Goal: Deleting a Goal
@goal_bp.route("/<goal_id>", methods = ["DELETE"])
def delete_one_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if not goal:
        return abort(make_response({"message": f"Goal {goal_id} is not found"}, 404))

    db.session.delete(goal)
    db.session.commit()

    response = {
        'details': f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
    }

    return make_response(response, 200)

@goal_bp.route("/<goal_id>/tasks", methods = ["POST"])
def add_tasks(goal_id):
    request_body = request.get_json()
    task_ids = request_body['task_ids']

    for task_id in task_ids:
        task = Task.query.get(task_id)
        if not task:
            return abort(make_response({"message": f"Task {task_id} is not found"}, 404))

        task.goal_id = goal_id

    db.session.commit()

    response_body = {
        "id": int(goal_id),
        "task_ids": task_ids
    }

    return make_response(jsonify(response_body), 200)

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_tasks(goal_id):
    goal = Goal.query.get(goal_id)

    if not goal:
        return abort(make_response({"message": f"Goal {goal_id} is not found"}, 404))


    tasks = []
    for task in goal.tasks:
        tasks.append(task.to_json())

    response_body = {
        "id": int(goal_id),
        "title": goal.title,
        "tasks": tasks
    }

    return make_response(jsonify(response_body), 200)