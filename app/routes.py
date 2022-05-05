from app import db
from app.models.task import Task 
from flask import Blueprint, jsonify, request, make_response


tasks_bp = Blueprint("tasks", __name__, url_prefix = "/tasks")

@tasks_bp.route('', methods=['POST'])
def create_task():
    request_body = request.get_json()
    new_task = Task (title = request_body['title'],
                    description = request_body['description'])

    db.session.add(new_task)
    db.session.commit()

    return {
        'id' : new_task.task_id
    }, 201