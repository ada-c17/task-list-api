from app import db
from app.models.task import Task
from app.models.goal import Goal
from app.task_routes import read_one_task
from flask import Blueprint, jsonify, abort, make_response, request

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=['POST'])
def create_goal():
    request_body = request.get_json()

    try:
        goal = Goal(title=request_body["title"])
    except KeyError as err:
        return make_response({"details": "Invalid data"}, 400)

    db.session.add(goal)
    db.session.commit()

    return make_response({"goal": {
                    "id": goal.goal_id,
                    "title": goal.title}}, 201)

@goals_bp.route("", methods=['GET'])
def read_goals():
    goals_response = []
    goals = Goal.query.all()
    for goal in goals:
        goals_response.append(
        {
            "id": goal.goal_id,
            "title": goal.title
        }
    )
    
    db.session.commit()
    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=['GET'])
def read_one_goal(goal_id):
    goal = validate_id(goal_id)

    db.session.commit()

    return {"goal": {
            "id": goal.goal_id,
            "title": goal.title,
    }
        }

@goals_bp.route("/<goal_id>", methods=['PUT'])
def update_goal_with_id(goal_id):
    goal = validate_id(goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return {"goal": {
            "id": goal.goal_id,
            "title": goal.title,
}
    }

@goals_bp.route("/<goal_id>", methods=['DELETE'])
def delete_goal(goal_id):
    goal = validate_id(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'})

@goals_bp.route("<goal_id>/tasks", methods=['POST'])
def send_task_ids_to_goal(goal_id):
    goal = validate_id(goal_id)
    request_body = request.get_json()

    for task in request_body["task_ids"]:
        task = Task.query.get(task)
        goal.tasks.append(task)

    db.session.commit()

    return {"id": goal.goal_id,
            "task_ids": [task.task_id for task in goal.tasks]
        }

@goals_bp.route("<goal_id>/tasks", methods=['GET'])
def get_tasks_for_goal(goal_id):
    goal = validate_id(goal_id)
        
    db.session.commit()
    return {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": [{"id": task.task_id, "title": task.title, "description": task.description, "goal_id": task.goal_id, "is_complete": task.is_complete()} for task in goal.tasks] 
    }

@goals_bp.route("/tasks/<task_id>", methods=['GET'])
def get_task_with_goal_id(task_id):
   pass


def validate_id(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message":f"goal {goal_id} invalid"}, 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message":f"goal {goal_id} not found"}, 404))

    return goal

    
