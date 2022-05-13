from flask import Blueprint, jsonify, request, make_response, abort
from app.models.goal import Goal
from app.models.task import Task
from app import db


goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

def validate_id(id):
    '''Validates that id is valid and exists'''
    try:
        id = int(id)
    except:
        abort(make_response({"msg": f"Invalid id: {id}"}, 400))
    
    result = Goal.query.get(id)
    if not result:
        abort(make_response({"msg": f"Could not find goal with id: {id}"}, 404))
    return result

def is_complete(task):
    '''Checks whether a task is incomplete or complete.'''
    if task.completed_at:
        return True
    else:
        return False

@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(
            title=request_body["title"] 
        )
    except KeyError:
        return {"details": "Invalid data"}, 400
    
    db.session.add(new_goal)
    db.session.commit()

    return {
        "goal": {
            "id": new_goal.goal_id,
            "title": new_goal.title
        }
    }, 201

@goal_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append({
            "id": goal.goal_id,
            "title": goal.title
        })
    return jsonify(goals_response)

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_id(goal_id)
    return {
        "goal": {
            "id": goal.goal_id,
            "title": goal.title
        }
    }

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_id(goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    return {
        "goal": {
            "id": goal.goal_id,
            "title": goal.title
        }
    }

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_id(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"}

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_goal_tasks(goal_id):
    goal = validate_id(goal_id)

    response_body = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": []
    }

    for task in goal.tasks:
        response_body["tasks"].append({
                "id": task.task_id,
                "goal_id": task.goal_id,
                "title": task.title,
                "description": task.description,
                "is_complete": is_complete(task)
        })
    
    return response_body, 200

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_goal_with_tasks(goal_id):
    goal = validate_id(goal_id)

    request_body = request.get_json()

    response_body = {
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
    }

    for task_id in request_body["task_ids"]:
        task = Task.query.get(task_id)
        if not task:
            return abort(make_response({"msg": f"Could not find task with id: {task.task_id}"}, 404))
        goal.tasks.append(task)

    db.session.commit()

    return response_body, 200
    