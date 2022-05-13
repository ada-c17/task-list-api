from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app.models.goal import Goal
from app import db
from app.task_routes import validate_task
from sqlalchemy import desc, asc
from datetime import datetime 

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_one_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal(title=request_body["title"])
        new_goal.title = request_body["title"]
    
        
    except KeyError:
        return {
            "details": "Invalid data"
        } , 400

    if "completed_at" in request_body:
        new_goal.completed_at = request_body["completed_at"]

    db.session.add(new_goal)
    db.session.commit()
    
    response = jsonify({"goal": {
        "id": new_goal.goal_id,
        "title": new_goal.title,}
    })
    return response, 201

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    params = request.args
    if "sort" in params :
        if params["sort"] == "desc":
            goals = Goal.query.order_by(desc(Goal.title)).all()
        else:
            goals = Goal.query.order_by(asc(Goal.title)).all()
    else:
        goals = Goal.query.all()

    goals_response = []
    #goals_response = [goal for goal in goals if goal in goals] ---> no time to fix this broken list comprehension >_< will get back to it

    for goal in goals:
        goals_response.append(
            {
                "id": goal.goal_id,
                "title": goal.title,
            }
        )
    return jsonify(goals_response), 200

# helper function on testing valid goals
def validate_goal(goal_id):
    try:
        goal = int(goal_id)
    except ValueError:
        response = {"details": f"Invalid id: {goal_id}"}
        abort(make_response(jsonify(response),400))
    chosen_goal = Goal.query.get(goal_id)

    if chosen_goal is None:
        response = {"details": f"Could not find goal with id #{goal_id}"}
        abort(make_response(jsonify(response),404))
    return chosen_goal


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    chosen_goal = validate_goal(goal_id)
    response = jsonify({"goal": {
        "id": chosen_goal.goal_id,
        "title": chosen_goal.title}
                
    })
    return response, 200    


@goals_bp.route("/<goal_id>", methods=["PUT"])
def replace_goal(goal_id):
    chosen_goal = validate_goal(goal_id)
    request_body = request.get_json()

    try:
        chosen_goal.title = request_body["title"]
        
    except KeyError:
        return {
            "details": "title is required"
        } , 400

    db.session.commit()
    response = jsonify({"goal": {
        "id": chosen_goal.goal_id,
        "title": chosen_goal.title,}
    })
    return response, 200


@goals_bp.route("/<goal_id>", methods = ["DELETE"])
def delete_goal(goal_id):
    chosen_goal = validate_goal(goal_id)
    db.session.delete(chosen_goal)
    db.session.commit()

    return {
        "details": f'Goal {chosen_goal.goal_id} "{chosen_goal.title}" successfully deleted'
    }, 200


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def send_task_list(goal_id):
    chosen_goal = validate_goal(goal_id)
    request_body = request.get_json()

    chosen_tasks = []

    for task_id in request_body["task_ids"]:
        chosen_task = validate_task(task_id)
        if chosen_task:
            chosen_tasks.append(chosen_task)
    
    chosen_goal.tasks = chosen_tasks

    db.session.commit()
    response = jsonify({
        "id": chosen_goal.goal_id,
        "task_ids": request_body["task_ids"]
    })
    return response, 200


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_one_goal(goal_id):
    chosen_goal = validate_goal(goal_id)
    response = {
        "id": chosen_goal.goal_id,
        "title": chosen_goal.title,
        "tasks": []

    }

    for task in chosen_goal.tasks:
        response["tasks"].append({
            "id": task.task_id,
            "goal_id": chosen_goal.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        })

    return jsonify(response), 200
    