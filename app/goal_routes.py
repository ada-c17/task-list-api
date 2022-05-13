from flask import Blueprint, request, jsonify
from app import db
from app.models.goal import Goal
from app.models.task import Task
from .helpers import validate_record

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# CREATE Goal
@goals_bp.route("", methods=["POST"])
def create_goal():
  request_body = request.get_json()

  new_goal = Goal.create(request_body)

  db.session.add(new_goal)
  db.session.commit()

  return jsonify({"goal": new_goal.to_json()}), 201


# GET ALL Goals 
@goals_bp.route("", methods=["GET"])
def get_all_goals():
  goals = Goal.query.all()

  goals_response = []

  for goal in goals: 
    goals_response.append(goal.to_json())
  
  return jsonify(goals_response), 200

# GET ONE Goal 
@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
  goal = validate_record(goal_id, Goal)

  return jsonify({"goal": goal.to_json()}), 200

# UPDATE Goal
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
  goal = validate_record(goal_id, Goal)
  
  request_body = request.get_json()

  goal.update(request_body)

  db.session.commit()

  return jsonify({"goal": goal.to_json()}), 200

# DELETE Goal
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
  goal = validate_record(goal_id, Goal)
  
  db.session.delete(goal)
  db.session.commit()

  return jsonify({"details": f'Goal {goal_id} \"{goal.title}\" successfully deleted'}), 200

# Add list of Task ids to a Goal:
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_task_ids_to_goal(goal_id):
	goal = validate_record(goal_id, Goal)

	request_body = request.get_json()

	for task_id in request_body["task_ids"]:
		task = validate_record(task_id, Task)
		goal.tasks.append(task) 

	db.session.commit()

	return jsonify({"id": goal.goal_id, "task_ids": request_body["task_ids"]}), 200

# Get Tasks of one Goal
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_one_goal(goal_id):
  goal = validate_record(goal_id, Goal)
  
  response_body = goal.to_json()
  
  response_body["tasks"] = [task.to_json() for task in goal.tasks]
  
  return jsonify(response_body), 200