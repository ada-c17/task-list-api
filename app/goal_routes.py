
from flask import Blueprint,  request
from app import db
from app.models.goal import Goal
from app.models.task import Task
from app.helper_functions import create_record_safely, success_message_info_as_list, return_database_info_dict, get_record_by_id, success_message_info_as_list, update_record_safely


goal_bp = Blueprint("Goals", __name__, url_prefix="/goals")

# Route functions

@goal_bp.route("", methods=["POST"])
def create_new_goal():
    request_body = request.get_json()
    new_goal = create_record_safely(Goal, request_body)

    db.session.add(new_goal)
    db.session.commit()

    return success_message_info_as_list(dict(goal=new_goal.self_to_dict()), 201)


@goal_bp.route("", methods=["GET"])
def get_all_goals():
    sort_param = request.args.get("sort")

    if sort_param == "asc":
        goals = Goal.query.order_by(Goal.title.asc())
    elif sort_param == "desc":
        goals = Goal.query.order_by(Goal.title.desc())
    else:
        goals = Goal.query.all()
    all_goals = [goal.self_to_dict() for goal in goals]
    return success_message_info_as_list(all_goals)


@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = get_record_by_id(Goal, goal_id)

    return return_database_info_dict("goal", goal.self_to_dict())


@goal_bp.route("/<goal_id>", methods=["PUT", "PATCH"])
def update_goal_by_id(goal_id):
    goal = get_record_by_id(Goal, goal_id)

    request_body = request.get_json()
    update_record_safely(Goal, goal, request_body)

    db.session.commit()

    return return_database_info_dict("goal", goal.self_to_dict())


@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = get_record_by_id(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return success_message_info_as_list(dict(details=f'Goal {goal.goal_id} "{goal.title}" successfully deleted'))



# Join Routes

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = get_record_by_id(Goal, goal_id)
    request_body = request.get_json()

    for elem in request_body["task_ids"]:
        task = get_record_by_id(Task, elem)
        goal.tasks.append(task)

    db.session.commit()

    return success_message_info_as_list(goal.return_id_and_task_ids_only())


@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_goal_with_tasks(goal_id):
    goal = get_record_by_id(Goal, goal_id)

    return success_message_info_as_list(goal.self_to_dict(True))

