from os import abort
from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request

from app.models.task import Task
from .helpers import validate_goal

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


# def validate_goal(goal_id):
#     try:
#         goal_id = int(goal_id)
#     except:
#         abort(make_response({"message":f"goal {goal_id} invalid"}, 400))

#     goal = Goal.query.get(goal_id)

#     if not goal:
#         abort(make_response({"message":f"goal {goal_id} not found"}, 404))

#     return goal



@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    try:
        request_body["title"]
    except:
        return {"details": "Invalid data"}, 400

    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    response_body = {}
    # response_body["goal"] = {
    #                         "id": new_goal.goal_id, 
    #                         "title": new_goal.title
    #                         }

    response_body["goal"] = new_goal.to_json()

    return response_body, 201



@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()
    goals_response = []

    for goal in goals:
        # goals_response.append({
        #     "id":goal.goal_id,
        #     "title": goal.title
        # })

        goals_response.append(goal.to_json())
    
    return jsonify(goals_response)


@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_goal(goal_id)

    response_body = {}
    # response_body["goal"] = {
    #         "id": goal.goal_id,
    #         "title": goal.title
    #     }
    response_body["goal"] = goal.to_json()

    return response_body


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    response_body = {}
    # response_body["goal"] = {
    #     "id": goal.goal_id,
    #     "title": goal.title
    # }
    response_body["goal"] = goal.to_json()
    return response_body


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_goal_many_tasks(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    for id in request_body["task_ids"]:
        task = Task.query.get(id)
        task.goal_id = goal.goal_id
        goal.tasks.append(task)

    db.session.commit()

    response_body = {
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
    }

    return response_body, 200



@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_tasks(goal_id):

    goal = validate_goal(goal_id)

    response_body = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": []
    }

    for task in goal.tasks:
        response_body["tasks"].append(
            {
            "id": task.task_id,
            "goal_id": task.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
            }
        )
    
    return jsonify(response_body), 200
