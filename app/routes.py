from flask import Blueprint, request, make_response, abort, jsonify
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_new_task():
    request_body = request.get_json()
    new_task = Task(
        title=request_body["title"],
        description=request_body["description"]
    )

    db.session.add(new_task)
    db.session.commit()

    return make_response(new_task.to_dict(), 201)

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    # Pull query parameters from url
    title_param = request.args.get("title")
    description_param = request.args.get("description")
    is_complete_param = request.args.get("is_complete")

    # start the query
    tasks = Task.query

    # build up the search criteria based on params present
    if title_param:
        tasks = tasks.filter_by(name=title_param)
    if description_param:
        tasks = tasks.filter_by(description=description_param)
    if is_complete_param:
        tasks = tasks.filter_by(color=is_complete_param)
    
    # execute the search and return all records that meet the criteria built
    tasks = tasks.all()
    

    return make_response(new_task.to_dict(), 201)