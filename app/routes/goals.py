from flask import Blueprint, request, jsonify, abort, make_response
from app import db
from app.models.goal import Goal
from app.models.task import Task
from sqlalchemy import desc, asc

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# Wave 5
@goals_bp.route("", methods=["GET"])
def read_all_goal():
    """
        - Getting all goals and returning in json response with 200
        - Returning empty list if no goal in database
    """
    

    params = request.args
    # sort by title
    if "sort" in params:
        if params["sort"].lower() == "desc" or params["sort"].lower() == "descending":
                chosen_goal = Goal.query.order_by( desc(Goal.title) ).all()
        else:
            chosen_goal = Goal.query.order_by( asc(Goal.title) ).all()
    # sort by id if no any query params
    else:
        chosen_goal = Goal.query.order_by(asc(Goal.id)).all()

    if len(chosen_goal) == 0:
        return jsonify([]), 200

    # get all goal from database
    response_body = [goal.goal_response_body_dict() for goal in chosen_goal]

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
    """Getting a goal by goal id and returning in json response with 200"""
    # validating goal id
    chosen_goal = validate_goal_id(goal_id)
    return jsonify({"goal": chosen_goal.goal_response_body_dict()}), 200


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
    """Adding a goal into database and returning added record in json response with 201"""
    # validating missing title in request or not
    request_goal = validate_title_key_for_post_or_update()
    
    new_gaol = Goal(
        title = request_goal["title"]
    )
    db.session.add(new_gaol)
    db.session.commit()

    return jsonify({"goal": new_gaol.goal_response_body_dict()}), 201


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    """Updating a goal by goal id and returning updated record in json response with 200"""
    # validating goal id
    chosen_goal = validate_goal_id(goal_id)
    # validating whether missing title key or not
    request_goal = validate_title_key_for_post_or_update()
    chosen_goal.title = request_goal["title"]
    db.session.commit()

    return jsonify({"goal": chosen_goal.goal_response_body_dict()}), 200


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal_id(goal_id):
    """Removing a goal by goal id and returning a message with 200"""
    chosen_goal = validate_goal_id(goal_id)
    db.session.delete(chosen_goal)
    db.session.commit()
    response_body = {"details": f'Goal {goal_id} "{chosen_goal.title}" successfully deleted'}
    return jsonify(response_body), 200


#Wave 6
# helper function to check task id
def get_task_or_abort(task_id):
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
    """Adding goal id into foreign key column of task table and returning json response object with 200"""
    # add task ids to goal
    chosen_goal = validate_goal_id(goal_id)
    request_task_list = request.get_json()
    # check if task_ids exist in request body and it is a list
    if "task_ids" in request_task_list and isinstance(request_task_list["task_ids"], list):
        tasks_list = request_task_list["task_ids"]
    else:
        abort(make_response({"message": "The input is invalid."}, 400))

    # set foreign key goal id in task table to specific goal
    for task_id in tasks_list:
        chosen_task = get_task_or_abort(task_id)
        if chosen_task.id == task_id and chosen_task.goal_id is None:
                chosen_task.goal_id = chosen_goal.id
    db.session.commit()

    response_body = {
        "id": chosen_goal.id,
        "task_ids": [task.id for task in chosen_goal.tasks]
    }

    return jsonify(response_body), 200


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_a_goal(goal_id):
    """Getting task list by a goal and returning a json response with 200"""
    # validating goal id
    chosen_goal = validate_goal_id(goal_id)
    response_body = {
        "id": chosen_goal.id,
        "title": chosen_goal.title,
        "tasks": [task.task_response_body_dict() for task in chosen_goal.tasks]
    }
    return jsonify(response_body), 200