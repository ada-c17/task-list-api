from operator import is_
from flask import Blueprint, request, make_response, jsonify, abort
from app import db
from app.models.task import Task 


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
# POST new task
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    new_task = Task(
        title=request_body["title"], 
        description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    if new_task.completed_at != None:
        new_task.is_complete = True

    response_body = jsonify({'task':
    {'id':new_task.task_id, 
    'title':new_task.title, 
    'description':new_task.description, 
    'is_complete':new_task.is_complete}
    })

    return response_body, 201

# GET all tasks
@tasks_bp.route('', methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id, 
            "title": task.title, 
            "description": task.description, 
            "is_complete": task.is_complete
        })

    return jsonify(tasks_response)
