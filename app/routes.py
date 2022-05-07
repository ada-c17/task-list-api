from operator import is_
from xmlrpc.client import ResponseError
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

    return jsonify({'task':
    {'id':new_task.task_id, 
    'title':new_task.title, 
    'description':new_task.description, 
    'is_complete':new_task.is_complete}
    }), 201

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


def validate_task_id(task_id):
    try: 
        task_id = int(task_id)
    except ValueError:
        abort(make_response({"msg":f"The task with id {task_id} is invalid"}, 400))
    
    tasks = Task.query.all()
    for task in tasks: 
        if task.task_id == task_id:
            return task

    abort(make_response({"msg":f"The task with id {task_id} is not found"}, 404))

# GET one task 
@tasks_bp.route('/<task_id>', methods=["GET"])
def get_one_task(task_id):
    task = validate_task_id(task_id)

    return jsonify({'task':
    {'id':task.task_id, 
    'title':task.title, 
    'description':task.description, 
    'is_complete':task.is_complete}
    })

@tasks_bp.route('/<task_id>', methods=["PUT"])
def update_task(task_id):
    task = validate_task_id(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    
    if task.completed_at != None:
        task.is_complete = True

    return jsonify({'task':
        {'id':task.task_id, 
        'title':task.title, 
        'description':task.description, 
        'is_complete':task.is_complete}
        })
