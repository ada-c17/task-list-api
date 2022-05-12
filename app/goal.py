from flask import Blueprint, make_response, request,jsonify, abort
from app import db
from app.models.goal import Goal
from app.models.task import Task

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message":f"Goal {goal_id} invalid"}, 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message":f"Goal {goal_id} not found"}, 404))

    return goal

@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        response_body = {"details": "Invalid data"}
        return response_body, 400
    else:
        new_goal = Goal(title = request_body["title"])

        db.session.add(new_goal)
        db.session.commit()

        response_body = {"goal":
            {
            "id": new_goal.goal_id,
            "title": new_goal.title
            }
        }
        return jsonify(response_body), 201

@goal_bp.route("", methods=["GET"])
def get_all_saved_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(
            {
                "id": goal.goal_id,
                "title": goal.title,
            }
        )
    return jsonify(goals_response), 200

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)

    return jsonify({"goal":
    {"id": goal.goal_id,
    "title": goal.title}
    }) 

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()
    
    response_body = {"goal":
        {"id": goal.goal_id,
        "title": goal.title}
        }
    return jsonify(response_body), 200

@goal_bp.route("/<goal_id>" , methods = ["DELETE"])
def delete_one_goal(goal_id):

    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    response_body = (f'Goal {goal.goal_id} "{goal.title}" successfully deleted')

    return make_response(jsonify({"details":response_body}))

def get_task_or_abort(list_of_task_id):
    try:
        list_of_task_id = int(list_of_task_id)
    except ValueError:
        abort(make_response({"message":f"Task {list_of_task_id} invalid"}, 400))

    task_id = Task.query.get(list_of_task_id)

    if not task_id:
        abort(make_response({"message":f"Task {list_of_task_id} not found"}, 404))

    return task_id


@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_tasks_to_goal(goal_id):

    goal = validate_goal(goal_id)

    request_body = request.get_json()
    try:
        list_of_task_id = request_body["task_ids"]
    except ValueError:
        return jsonify({"message": "Missing list_of_task_id in request body"}, 400)

    if not isinstance(list_of_task_id,list):
        return jsonify({'msg': "Expected list of task_id IDs"}), 400

    for task_id in list_of_task_id:
        task = get_task_or_abort(task_id)
        task.goal_id = goal.goal_id

    db.session.commit()
    return make_response(jsonify({
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
    }))

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_to_goal(goal_id):
    goal = validate_goal(goal_id)

    tasks = Task.query.all()
    response_body = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": []
    }

    for task_id in tasks:
        if task_id.goal_id == goal.goal_id: #333 == 333
            response_body["tasks"].append(task_id.to_dict())
    db.session.commit()
    return jsonify(response_body), 200