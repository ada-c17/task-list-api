from flask import Blueprint, jsonify, make_response, request
from app.models.task import Task
from app import db


bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@bp.route("", methods=("POST",))
def create_task():
    request_body = request.get_json()
    
    new_task = Task(title=request_body["title"], description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    return make_response({
        "task": {
            "title": new_task.title, 
            "description": new_task.description, 
            "id": new_task.task_id, 
            "is_complete": new_task.completed_at
            }
    }), 201

    # return make_response(Task.to_dict(new_task))