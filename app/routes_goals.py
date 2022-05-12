from flask import Blueprint, jsonify, request, abort, make_response
from .models.task import Task
from .models.goal import Goal
from app import db
from .routes_tasks import complete_or_not, validate_task, get_all_tasks

goal_bp = Blueprint("", __name__, url_prefix="/goals" )


# helper function:
def validate_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        abort(make_response({"message":f"goal {goal_id} not found"}, 404))
    return goal

# CREATE (CRUD)
# POST request to /goals
# request_body = {"title": "My New Goal"}

@goal_bp.route("", methods=['POST'])
def create_one_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(title=request_body['title'])
    except:
        return jsonify({"details": "Invalid data"}), 400
    db.session.add(new_goal)
    db.session.commit()
    response = {"goal": new_goal.to_dict()}    
    return jsonify(response), 201


# READ (CRUD): aka GET
@goal_bp.route("", methods=['GET'])
def get_all_goals():
    goals = Goal.query.all()
    goal_list = []
    for goal in goals:
        goal_list.append(goal.to_dict())
    return jsonify(goal_list), 200

@goal_bp.route("/<goal_id>",methods=["GET"])
def get_goal_by_id(goal_id):
    goal = validate_goal(goal_id)
    response = { 'goal': goal.to_dict()}
    return jsonify(response), 200

# UPDATE(CRUD): aka PATCH/PUT
@goal_bp.route("/<goal_id>",methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    goal.title = request_body['title']
    db.session.commit()
    response = {"goal": goal.to_dict()}
    return jsonify(response), 200

# DELETE (CRUD)
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal = validate_goal(goal_id)
    db.session.delete(goal)
    db.session.commit()
    response = {
        "details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
    }
    return jsonify(response), 200

# adding tasks to a goal: CREATE (CRUD) aka POST
# request body: {"task_ids": [1, 2, 3]}  These are the tasks to add to the goal_id
# response expected: { "id": 1,"task_ids": [1, 2, 3]} where id is goal_id

@goal_bp.route("/<goal_id>/tasks", methods = ["POST"])
def add_task_to_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    task_id_list = request_body['task_ids']
    for task_id in task_id_list:
        task = validate_task(task_id)
        task.goal_id = goal_id 
        db.session.commit()
    response = {
        "id": int(goal_id),
        "task_ids": task_id_list}

    return jsonify(response), 200

# getting tasks; Read (CRUD)
# example endpoint: /goals/333/tasks ...where 333 is <goal_id>
# example response: {"id": 333,"title": "Build a habit of going outside daily",
#   "tasks": [{"id": 999,"goal_id": 333,"title": "Go on my daily walk 🏞","description": "Notice something new every day",
#   "is_complete": false }]}

@goal_bp.route("/<goal_id>/tasks", methods = ['GET'])
def get_tasks_of_goal(goal_id):
    goal = validate_goal(goal_id)
    tasks = goal.tasks  # task objects
    task_list = []
    for task in tasks:
        task = validate_task(task.task_id)
        task_list.append(task.to_dict())

    response = { "id": int(goal_id),
    "title": goal.title,
    "tasks": task_list}
    return jsonify(response), 200