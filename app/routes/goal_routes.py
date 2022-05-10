from app import db
from app.models.goal import Goal
from app.models.task import Task
from app.routes.task_routes import validate_task
from flask import Blueprint, request, make_response, jsonify, abort


goals_bp = Blueprint("goal", __name__, url_prefix="/goals")

# Validate Goal ID
def validate_goal(id):
    try:
        goal_id = int(id)
    except:
        return abort(make_response(jsonify("Goal is invalid"), 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        return abort(make_response(jsonify(f"Goal {id} does not exist"), 404))
    return goal

# Get all goals
@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all() 

    goals_response = []
    for goal in goals:
        goals_response.append({
            "id":goal.id,
            "title":goal.title,
            })
    return make_response(jsonify(goals_response), 200)

# Get one goal
@goals_bp.route("/<id>", methods=["GET"])
def get_one_goal(id):
    goal = validate_goal(id)
    response_body = {}

    response_body["goal"] = {
        "id":goal.id,
        "title":goal.title,
        }
    
    return make_response(jsonify(response_body), 200)

# Create a goal
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal(title=request_body["title"])
    except KeyError:
        return abort(make_response(jsonify({"details":"Invalid data"}), 400))

    db.session.add(new_goal)
    db.session.commit()

    response_body = {}
    response_body["goal"] = {
            "id":new_goal.id,
            "title":new_goal.title
            }

    return make_response(jsonify(response_body), 201)

# Update a goal
@goals_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_goal(id)
    request_body = request.get_json()

    try:
        goal.title = request_body["title"]
    except KeyError:
        return abort(make_response(jsonify({"details":"Invalid data"}), 400))

    db.session.commit()
    
    response_body = {}
    response_body["goal"] = {
            "id":goal.id,
            "title":goal.title
            }
    
    return make_response(jsonify(response_body), 200)

# Delete a goal
@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = validate_goal(id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({'details':f'Goal {goal.id} "{goal.title}" successfully deleted'}), 200)

# Post Task IDs to a GOAL
@goals_bp.route("/<id>/tasks", methods=["POST"])
def post_task_ids_to_goal(id):
    goal = validate_goal(id)
    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        validate_task(task_id)
        task = Task.query.get(task_id)
        task.goal_id = goal.id
    
    db.session.commit()
    
    response_body = {}
    response_body = {
            "id":goal.id,
            "task_ids": request_body["task_ids"]
            }
    
    return make_response(jsonify(response_body), 200)

# Get tasks for one specific goal
@goals_bp.route("/<id>/tasks", methods=["GET"])
def get_all_tasks_by_goal(id):
    goal = validate_goal(id)
    
    tasks_response = []
    for task in goal.tasks:
        tasks_response.append({
            "id":task.id,
            "goal_id": task.goal_id,
            "title":task.title,
            "description":task.description,
            "is_complete": True if task.completed_at else False
            })
    
    response_body = {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_response
    }

    return make_response(jsonify(response_body), 200)
