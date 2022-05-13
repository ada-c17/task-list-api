from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.goal import Goal
from app.models.task import Task
from app.task_routes import validate_task

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

# create a new goal
@goals_bp.route("", methods=["POST"])
def create_goal():
    if not request.get_json():
        abort(make_response({"details": "Invalid data"}, 400))
    
    request_body = request.get_json()
    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    response_body = {"goal": new_goal.to_dict()}

    return make_response(jsonify(response_body), 201)

# get all goals
@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    goals_response = [goal.to_dict() for goal in goals]

    return jsonify(goals_response)

# get goal by id
@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal_by_id(goal_id):
    goal = validate_goal(goal_id)
    return {"goal": goal.to_dict()}

# update goal by id
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    
    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()
    return {"goal": goal.to_dict()}

# delete goal by id
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f'Goal {goal_id} \"{goal.title}\" successfully deleted'})

# get tasks by goal id
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    goal = validate_goal(goal_id)
    task_list = [task.to_dict() for task in goal.tasks]

    goal_dict = goal.to_dict()
    goal_dict["tasks"] = task_list

    return jsonify(goal_dict)

# post tasks to goal by goal id
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_tasks_to_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        task = Task.query.get(task_id)
        task.goal_id = goal_id
        task.goal = goal

    db.session.commit()

    return make_response({
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
    })

# helper function to validate goal by id
def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"details": f"Goal #{goal_id} invalid"}, 400))
    
    goal = Goal.query.get(goal_id)
    
    if not goal:
        abort(make_response({"details": f"Goal #{goal_id} not found"}, 404))
    
    return goal