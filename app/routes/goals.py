from app import db
from flask import Blueprint, jsonify, make_response, request, abort
from app.models.goal import Goal
from app.models.task import Task
from app.routes.request_helpers import handle_id_request, check_complete_request_body

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals_list = []

    goals = Goal.query.all()
    
    for goal in goals:
        goals_list.append(goal.make_response_dict())
    
    return make_response(jsonify(goals_list), 200)


@goals_bp.route("/<id>", methods=["GET"])
def get_goal_by_id(id):
    goal = handle_id_request(id, Goal)
    return make_response(jsonify({"goal": goal.make_response_dict()}), 200)


@goals_bp.route("", methods=["POST"])
def create_new_goal():
    request_body = check_complete_request_body(request, Goal)
    new_goal = Goal().create_from_request(request_body)

    db.session.add(new_goal)
    db.session.commit()

    confirmation_msg = {"goal": new_goal.make_response_dict()}
    return make_response(jsonify(confirmation_msg), 201)

@goals_bp.route("/<id>", methods=["PUT"])
def update_goal_by_id(id):
    request_body = check_complete_request_body(request, Goal)
    active_goal = handle_id_request(id, Goal)

    active_goal.create_from_request(request_body)

    db.session.commit()
    confirmation_msg = {"goal": active_goal.make_response_dict()}
    return make_response(jsonify(confirmation_msg), 200)

@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal_by_id(id):
    goal_to_delete = handle_id_request(id, Goal)

    db.session.delete(goal_to_delete)
    db.session.commit()

    confirmation_msg = {"details": f"Goal {id} \"{goal_to_delete.title}\" successfully deleted"}
    return make_response(jsonify(confirmation_msg), 200)

@goals_bp.route("/<id>/tasks", methods=["POST"])
def add_list_of_tasks_to_goal(id):
    handle_id_request(id, Goal)
    id = int(id)

    bad_request_msg = {"msg":"Invalid input. Use {\"task_ids\": [1, 2,...]}. IDs must be int."}
    try:
        task_ids = request.get_json()["task_ids"]
    except KeyError:
        abort(make_response(jsonify(bad_request_msg), 400))
    if not type(task_ids) == list or not all(type(task_id) == int 
                                            for task_id in task_ids):
        abort(make_response(jsonify(bad_request_msg), 400))

    response_ids = []
    invalid_ids = []
    for task in task_ids:
        active_task = Task.query.get(task)
        #for out-of-range task ids, nothing happens
        if active_task:
            active_task.goal_id = id
            response_ids.append(int(task))
        else:
            invalid_ids.append(int(task))

    db.session.commit()

    confirmation_msg = {"id": id, "task_ids": response_ids}
    if invalid_ids:
        confirmation_msg["invalid_ids"] = invalid_ids
    return make_response(jsonify(confirmation_msg), 200)

@goals_bp.route("/<id>/tasks", methods=["GET"])
def get_task_list_by_goal_id(id):
    active_goal = handle_id_request(id, Goal)
    response_body = active_goal.make_response_dict()

    task_list = []
    for task in active_goal.tasks:
        task_list.append(task.make_response_dict())

    response_body["tasks"] = task_list

    return make_response(jsonify(response_body), 200)