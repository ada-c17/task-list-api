from flask import Blueprint, request, make_response, jsonify
from app import db
from app.models.task import Task
from .helpers import validate_record, send_slack_message
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# CREATE Task
@tasks_bp.route("", methods=["POST"])
def create_task(): 
  request_body = request.get_json()
  
  new_task = Task.create(request_body)

  db.session.add(new_task)
  db.session.commit()

  return make_response({"task": new_task.to_json()}, 201)

#GET ALL Tasks and filter with params
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
  sort_query = request.args.get("sort")

  if sort_query == "asc":
    tasks = Task.query.order_by(Task.title.asc())
  elif sort_query == "desc":
    tasks = Task.query.order_by(Task.title.desc())
  else:
    tasks = Task.query.all()

  tasks_response = []

  for task in tasks:
    tasks_response.append(task.to_json())

  return jsonify(tasks_response), 200

# GET ONE Task 
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
  task = validate_record(task_id, Task)

  return jsonify({"task": task.to_json()}), 200

# UPDATE Task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
  task = validate_record(task_id, Task)
  request_body = request.get_json()

  task.update(request_body)

  db.session.commit()

  return make_response({"task":task.to_json()}, 200)

# DELETE Task 
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
  task = validate_record(task_id, Task)

  db.session.delete(task)
  db.session.commit()

  return jsonify({"details": f'Task {task_id} \"{task.title}\" successfully deleted'}), 200

# Mark Task Complete & send slack message 
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
  task = validate_record(task_id, Task)

  send_slack_message(f"Someone just completed the task {task.title}")
  
  task.completed_at = datetime.now()

  db.session.commit()
  return jsonify({"task": task.to_json()}), 200

# Mark Task Incomplete
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
  task = validate_record(task_id, Task)

  task.completed_at = None
  db.session.commit()

  return jsonify({"task": task.to_json()}), 200