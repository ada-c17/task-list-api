from app import db
from app.models.task import Task 
from flask import Blueprint, jsonify, request, make_response


tasks_bp = Blueprint("tasks", __name__, url_prefix = "/tasks")


@tasks_bp.route('', methods=['POST'])
def create_task():
    request_body = request.get_json()
    new_task = Task(title = request_body['title'],
                    description = request_body['description'])

    db.session.add(new_task)
    db.session.commit()

    return {
        "task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": False
    }
},201

@tasks_bp.route('', methods=['GET'])
def list_all_tasks():
    tasks = Task.query.all()
    task_response = []
    for task in tasks:
        task_response.append(
            {
                "id":task.task_id,
                "title":task.title,
                "description":task.description,
                "is_complete": False 
            }
        )
    return jsonify(task_response)

@tasks_bp.route("/<task_id>", methods=['GET'])
def get_one_task(task_id):
    task = Task.query.get(task_id)
    return{
                "task": {
                "id":task.task_id,
                "title":task.title,
                "description":task.description,
                "is_complete": False 
            }
    }

@tasks_bp.route("/<task_id>", methods=['PUT'])
def update_one_task(task_id, ):
    task = Task.query.get(task_id)
    
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    return{
                "task": {
                "id":task.task_id,
                "title":task.title,
                "description":task.description,
                "is_complete": False 
            }
    }