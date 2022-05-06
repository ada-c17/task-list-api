from os import abort
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request


# ---- CREATING BLUEPRINT INSTANCE---- # 
task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


# ---- HELPER FUNCTIONS ---- #

# def validate_task(task_id):
#     try:
#         task_id = int(task_id)
#     except:
#         abort(make_response({"message" : f"Task {task_id} is invalid."}, 400))

#     for task in tasks:
#         if task.id == task_id:
#             return task
    
#     abort(make_response({"message" : f"Task {task_id} is not found."}, 404))

# ---- ROUTE FUNCTIONS ---- #

# class Task(db.Model):
#     task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     title = db.Column(db.String)
#     description = db.Column(db.String)
#     completed_at = db.Column(db.DateTime, nullable=True)

# ---- READ ALL TASKS ---- #
# @task_bp.route("", methods=["GET"])
# def read_all_tasks():
    
#     tasks_response = []

#     tasks = Task.query.all()

#     for task in tasks:
#         tasks_response.append({
#             "id" : task.id,
#             "title" : task.title,
#             "description" : task.description
#         })
    
#     return jsonify(tasks_response)

# ---- READ ONE TASK BY ID ---- #
# @task_bp.route("/<task_id>", methods=["GET"])
# def read_one_task(task_id):
#     task = validate_task(task_id)

#     return {
#         "id" : task.id,
#         "title" : task.title,
#         "description" : task.description,
#     }


# ---- CREATE A TASK ---- #
@task_bp.route("", methods=["POST"])
def create_task():
    
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    # NEED TO FIX THIS RESPONSE
    return make_response(jsonify("new task created", 201))
