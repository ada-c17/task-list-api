from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request
from .helpers import call_slack, validate_goal


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# POST ROUTES


@goals_bp.route("", methods=["POST"])
def add_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    new_goal = Goal.create(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal": new_goal.to_json()}, 201)

# GET ROUTES


@ goals_bp.route("", methods=["GET"])
def read_all_goals():
    # sort_order = request.args.get("sort")

    # if sort_order == "asc":
    #     tasks = Task.query.order_by(Task.title.asc())
    # elif sort_order == "desc":
    #     tasks = Task.query.order_by(Task.title.desc())
    # else:
    goals = Goal.query.all()

    response = [goal.to_json() for goal in goals]

    return jsonify(response), 200


@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_goal(goal_id)
    return make_response({"goal": goal.to_json()}, 200)

# PUT ROUTES


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    goal.update(request_body)

    db.session.commit()

    return make_response({"goal": goal.to_json()}, 200)

# DELETE ROUTES


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal = validate_goal(goal_id)
    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"}, 200)

# # PATCH ROUTES


# @ tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
# def mark_task_complete(task_id):
#     task = validate(task_id)
#     task.completed_at = date.today()

#     db.session.commit()
#     call_slack(f"Someone just completed the task {task.title}")
#     return make_response({"task": task.to_json()}, 200)


# @ tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
# def mark_task_incomplete(task_id):
#     task = validate(task_id)
#     task.completed_at = None

#     db.session.commit()
#     return make_response({"task": task.to_json()}, 200)
