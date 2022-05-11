from calendar import c
from urllib import response
from flask import Blueprint, request, jsonify, abort, make_response
from app import db
from app.models.goal import Goal
from app.models.task import Task

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# Wave 5
@goals_bp.route("", methods=["GET"])
def read_all_goal():
    chosen_goal = Goal.query.all()

    if len(chosen_goal) == 0:
        return jsonify([]), 200

    response_body = []
    for goal in chosen_goal:
        response_body.append({
            "id": goal.id,
            "title": goal.title
        })

    return jsonify(response_body), 200


# helper function to check task id
def validate_goal_id(goal_id):
    """
    Checking the id goal from input:
        - return object goal if id is integer
        - raise exception if id is not integer then return status code 400,
        but if the id not exist then return status code 404

    """
    try:
        goal_id = int(goal_id)
    except ValueError:
        abort(make_response({"message": f"The goal id {goal_id} is invalid. The id must be integer."}, 400))
    
    goals = Goal.query.all()
    for goal in goals:
        if goal.id == goal_id:
            return goal
    abort(make_response({"message": f"The goal id {goal_id} is not found"}, 404))


@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal_id(goal_id):
    chosen_goal = validate_goal_id(goal_id)
    response_body = {
        "goal": {
            "id": chosen_goal.id,
            "title": chosen_goal.title
        }
    }
    return jsonify(response_body), 200


# helper function to check key dictionary exist or not
def validate_title_key_for_post_or_update():
    """Checking missing title key when post or update
        - raise exception if the key doesn't exist
        - return request object if the key exist
    """
    request_goal = request.get_json()
    if "title" not in request_goal:
        abort(make_response({"details": "Invalid data"}, 400))
    return request_goal


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_goal = validate_title_key_for_post_or_update()
    new_gaol = Goal(
        title = request_goal["title"]
    )

    db.session.add(new_gaol)
    db.session.commit()

    response_body = {
        "goal": {
            "id": new_gaol.id,
            "title": new_gaol.title
        }
    }

    return jsonify(response_body), 201


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    chosen_goal = validate_goal_id(goal_id)
    request_goal = validate_title_key_for_post_or_update()
    chosen_goal.title = request_goal["title"]
    db.session.commit()

    response_body = {
        "goal": {
            "id": chosen_goal.id,
            "title": chosen_goal.title
        }
    }

    return jsonify(response_body), 200


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal_id(goal_id):
    chosen_goal = validate_goal_id(goal_id)
    db.session.delete(chosen_goal)
    db.session.commit()
    response_body = {"details": f'Goal {goal_id} "{chosen_goal.title}" successfully deleted'}
    return jsonify(response_body), 200


#Wave 6
# helper function to check task id
def validate_task_id(task_id):
    """
    Checking the id task from input:
        - return object task if id is integer
        - raise exception if id is not integer then return status code 400,
        but if the id not exist then return status code 404

    """
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({"message": f"The task id {task_id} is invalid. The id must be integer."}, 400))
    
    tasks = Task.query.all()
    for task in tasks:
        if task.id == task_id:
            return task
    abort(make_response({"message": f"The task id {task_id} is not found"}, 404))

@goals_bp.route("/<goal_id>/tasks", methods=["POST"]) 
def post_task_ids_to_goal(goal_id):
    # add task ids to goal
    chosen_goal = validate_goal_id(goal_id)
    request_task_list = request.get_json()
    if "task_ids" in request_task_list:
        tasks_list = request_task_list["task_ids"]
    for task_id in tasks_list:
        chosen_task = validate_task_id(task_id)
        if chosen_task.id == task_id and not chosen_task.goal_id:
                chosen_task.goal_id = chosen_goal.id
    db.session.commit()

    # get all task ids list for one goal
    tasks = Task.query.all()
    task_ids = []
    for task in tasks:
        if task.goal_id == chosen_goal.id:
            task_ids.append(task.id)
    
    response_body = {
        "id": chosen_goal.id,
        "task_ids": task_ids
    }

    return jsonify(response_body), 200


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_a_goal(goal_id):
    chosen_goal = validate_goal_id(goal_id)
    response_body = {
        "id": chosen_goal.id,
        "title": chosen_goal.title,
        "tasks": []
    }

    for task in chosen_goal.tasks:
        #if task.id == tasks.goal_id:
        response_body["tasks"].append(task.task_response_body())
    
    return jsonify(response_body), 200