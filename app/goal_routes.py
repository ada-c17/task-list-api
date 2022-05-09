from app import db
from flask import Blueprint, request,make_response, abort,jsonify
from app.models.task import Task
from app.models.goal import Goal
#from app.models.goal.Goal import check_goal_JSON_request_body
from .task_routes import validate_task
from datetime import datetime

#Helper Functions:
def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message": f"Goal {goal_id} invalid"}, 400))
    
    goal = Goal.query.get(goal_id)
    if not goal:
        abort(make_response({"details": "Not found"}, 404))
    return goal

def check_goal_request_body():

    request_body = request.get_json()

    if "title" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    return request_body

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods = ["POST"])
def post_one_goal():

    request_body = check_goal_request_body()

    #request_body = check_goal_JSON_request_body()

    new_goal = Goal(title= request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return(make_response(jsonify(new_goal.goal_to_JSON()), 201))

@goals_bp.route("", methods = ["GET"])
def get_all_goals():

    params = request.args
    if params:
        if params["sort"] == "asc":
            tasks = Goal.query.order_by(Goal.title.asc()).all()
        elif params["sort"] == "desc":
            tasks= Goal.query.order_by(Goal.title.desc()).all()
    else:
        goals = Goal.query.all()

    goals_response = [goal.goal_to_JSON()["goal"] for goal in goals]

    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods = ["PUT"])
def update_one_goal(goal_id):

    chosen_goal = validate_goal(goal_id)
    request_body = check_goal_request_body()
    
    chosen_goal.title = request_body["title"]

    db.session.commit()

    return chosen_goal.goal_to_JSON()

@goals_bp.route("/<goal_id>", methods = ["GET"])
def get_one_goal(goal_id):

    chosen_goal = validate_goal(goal_id)

    return chosen_goal.goal_to_JSON()

@goals_bp.route("/<goal_id>", methods = ["DELETE"])
def delete_one_goal(goal_id):

    chosen_goal = validate_goal(goal_id)

    db.session.add(chosen_goal)
    db.session.commit()

    return (make_response({"details": f"Goal {goal_id} \"{chosen_goal.title}\" successfully deleted"}), 200)

@goals_bp.route("/<goal_id>/tasks", methods = ["POST"])
def post_task_to_specific_goal(goal_id):
    
    goal = validate_goal(goal_id)

    request_body = request.get_json()

    if "task_ids" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    
    for task_id in request_body["task_ids"]:
        task = validate_task(task_id)
        task.goal_id = goal_id
    
    db.session.commit()

    return make_response({
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
    })

@goals_bp.route("/<goal_id>/tasks", methods = ["GET"])
def get_tasks_to_specific_goal(goal_id):
    goal = validate_goal(goal_id)
    # tasks_response = [task.task_to_JSON()["task"] for task in goal.tasks]
    tasks_response = []
    for task in goal.tasks:
        tasks_response.append({
            "id": task.task_id,
            "goal_id": task.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        })
    return make_response({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks_response
    })