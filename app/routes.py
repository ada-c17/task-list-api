from app import db
from flask import Blueprint, request,make_response, abort,jsonify
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#Helper Functions:
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"details": f"Task {task_id} invalid"}, 400))
    
    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"details": "Not found"}, 404))
    return task

def check_task_request_body():

    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        abort(make_response({"details":"Invalid data"},400))

    return request_body

#Route Functions:
@tasks_bp.route("", methods = ["POST"])
def post_new_task():

    request_body = check_task_request_body()

    if "completed_at" in request_body:
        new_task = Task(title = request_body["title"],
                    description = request_body["description"],
                    completed_at = datetime.utcnow(),is_complete = True)
    else:
        new_task = Task(title = request_body["title"],
                        description = request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    return (make_response({"task":
            {"id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": new_task.is_complete,
        }}, 201))

@tasks_bp.route("", methods = ["GET"])
def get_all_tasks():

    params = request.args
    if params:
        if params["sort"] == "asc":
            tasks = Task.query.order_by(Task.title.asc()).all()
        elif params["sort"] == "desc":
            tasks= Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.is_complete
        }
        )
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):

    chosen_task = validate_task(task_id)

    return jsonify({"task":
            {"id": chosen_task.task_id,
            "title": chosen_task.title,
            "description": chosen_task.description,
            "is_complete": chosen_task.is_complete
        }})

@tasks_bp.route("/<task_id>", methods = ["PUT"])
def update_one_task(task_id):

    chosen_task = validate_task(task_id)
    request_body = check_task_request_body()

    if "completed_at" in request_body:
        chosen_task.title = request_body["title"]
        chosen_task.description = request_body["description"]
        chosen_task.completed_at = datetime.utcnow()
        chosen_task.is_complete = True
    else:
        chosen_task.title = request_body["title"]
        chosen_task.description = request_body["description"]

    db.session.commit()

    return (make_response({"task":
            {"id": chosen_task.task_id,
            "title": chosen_task.title,
            "description": chosen_task.description,
            "is_complete": chosen_task.is_complete,
        }}, 200))

@tasks_bp.route("/<task_id>", methods = ["DELETE"])
def delete_one_task(task_id):
    chosen_task = validate_task(task_id)

    db.session.delete(chosen_task)
    db.session.commit()

    return (make_response({"details":f"Task {task_id} \"{chosen_task.title}\" successfully deleted"}), 200)


@tasks_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
def patch_mark_complete(task_id):

    chosen_task = validate_task(task_id)

    chosen_task.completed_at = datetime.utcnow()
    chosen_task.is_complete = True

    db.session.commit()
    
    return (make_response({"task":
            {"id": chosen_task.task_id,
            "title": chosen_task.title,
            "description": chosen_task.description,
            "is_complete": chosen_task.is_complete,
        }}, 200))

@tasks_bp.route("/<task_id>/mark_incomplete", methods = ["PATCH"])
def patch_mark_incomplete(task_id):

    chosen_task = validate_task(task_id)

    chosen_task.completed_at = None
    chosen_task.is_complete = False

    db.session.commit()
    
    return (make_response({"task":
            {"id": chosen_task.task_id,
            "title": chosen_task.title,
            "description": chosen_task.description,
            "is_complete": chosen_task.is_complete,
        }}, 200))


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

#Helper Functions:
def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message": f"Goal {goal_id} invalid"}, 400))
    
    goal = Goal.query.get(goal_id)
    if not goal:
        abort(make_response({"details": "Not found"}, 404))
    return goal

def check_goal_request_body():

    request_body = request.get_json()

    if"title" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    return request_body

@goals_bp.route("", methods = ["POST"])
def post_one_goal():

    request_body = check_goal_request_body()

    new_goal = Goal(title= request_body["title"] )

    db.session.add(new_goal)
    db.session.commit()

    return(make_response(jsonify({"goal": {
        "id": new_goal.goal_id,
        "title": new_goal.title
    }}), 201))

@goals_bp.route("", methods = ["GET"])
def get_all_goals():

    goals_response = []

    goals = Goal.query.all()
    for goal in goals:
        goals_response.append({
            "id": goal.goal_id,
            "title": goal.title
        })
    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods = ["PUT"])
def update_one_goal(goal_id):

    chosen_goal = validate_goal(goal_id)
    request_body = check_goal_request_body()
    
    chosen_goal.title = request_body["title"]

    db.session.commit()

    return jsonify({"goal": {
        "id": chosen_goal.goal_id,
        "title": chosen_goal.title
    }})

@goals_bp.route("/<goal_id>", methods = ["GET"])
def get_one_goal(goal_id):

    chosen_goal = validate_goal(goal_id)

    return jsonify({"goal": {
        "id": chosen_goal.goal_id,
        "title": chosen_goal.title
    }})

@goals_bp.route("/<goal_id>", methods = ["DELETE"])
def delete_one_goal(goal_id):

    chosen_goal = validate_goal(goal_id)

    db.session.add(chosen_goal)
    db.session.commit()

    return (make_response({"details": f"Goal {goal_id} \"{chosen_goal.title}\" successfully deleted"}), 200)

