from flask import Blueprint, request, make_response, jsonify
from app.models.task import Task
from app.models.goal import Goal
from app import db
from app.routes.helper_routes import validate_id, validate_request


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_new_goal():
    request_body = validate_request(request, "title")
    new_goal = Goal(
        title=request_body["title"]
    )
    db.session.add(new_goal)
    db.session.commit()
    return make_response({"goal": new_goal.to_dict()}, 201)

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    title_param = request.args.get("title")
    goals = Goal.query
    if title_param:
        goals = goals.filter_by(title=title_param)
    goals = goals.all()
    goals_response = [goal.to_dict() for goal in goals]
    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_id(Goal, goal_id)
    return {"goal": goal.to_dict()}

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_id(Goal, goal_id)
    request_body = validate_request(request, "title")
    goal.title = request_body["title"]
    db.session.commit()
    return make_response(jsonify({"goal": goal.to_dict()}))

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_id(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return make_response({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'})

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_from_one_goal(goal_id):
    goal = validate_id(Goal, goal_id)
    response = goal.to_dict()
    response["tasks"] = goal.get_tasks()
    return make_response(response)

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def connect_tasks_to_goal(goal_id):
    goal = validate_id(Goal, goal_id)
    request_body = validate_request(request, "task_ids")
    for task_id in request_body["task_ids"]:
        goal.tasks.append(Task.query.get(task_id))
    db.session.commit()
    response = {"id": goal.goal_id, "task_ids": goal.get_task_ids()}
    return make_response(response)
