from flask import Blueprint, jsonify, request, make_response, abort
from app.models.goal import Goal
from app.models.task import Task
from app import db


goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")


@goal_bp.route("", methods=["POST"])
def create_goal():
    '''Creates a new Goal record. Title is only required param.'''
    request_body = request.get_json()
    try:
        new_goal = Goal(title=request_body["title"])
    except KeyError:
        return {"details": "Invalid data"}, 400
    
    db.session.add(new_goal)
    db.session.commit()

    return {"goal": Goal.goal_response(new_goal)}, 201


@goal_bp.route("", methods=["GET"])
def get_all_goals():
    '''Returns all Goals. Default sorted by id.'''
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(Goal.goal_response(goal))
    return jsonify(goals_response)


@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    '''Request information about a specific Goal.'''
    goal = Goal.validate_goal(goal_id)
    return {"goal": Goal.goal_response(goal)}


@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    '''Update a Goal record.'''
    goal = Goal.validate_goal(goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    return {"goal": Goal.goal_response(goal)}


@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    '''Deletes a Goal. Can not be undone.'''
    goal = Goal.validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"}


@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_goal_tasks(goal_id):
    '''Gets all Tasks associated with a Goal.'''
    goal = Goal.validate_goal(goal_id)
    response_body = Goal.goal_response(goal)
    response_body["tasks"] = []
    for task in goal.tasks:
        response_body["tasks"].append(Task.task_response(task))
    return response_body, 200


@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_goal_with_tasks(goal_id):
    '''Assigns existing tasks to an existing goal.'''
    goal = Goal.validate_goal(goal_id)
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
