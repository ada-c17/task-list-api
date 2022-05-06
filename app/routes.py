from flask import Blueprint, request, make_response, jsonify, abort
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "POST":
        request_body = request.get_json()
        try:
            task = Task(
                title = request_body["title"],
                description = request_body["description"]
                )
        except:
            abort(make_response({"details":"Invalid data"}, 400))

        db.session.add(task)
        db.session.commit()

        return make_response(
            jsonify({"task":display_task(task)}), 201
        )

    elif request.method == "GET":
        
        tasks = Task.query.all()

        param = request.args.get("sort")
        if param:
            is_desc = True if param == "desc" else False
            tasks.sort(reverse=is_desc, key=lambda task:task.title)
            
        res = []
        for task in tasks:
            res.append(
                display_task(task)
            )
        return make_response(jsonify(res), 200)

@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(task_id):
    task = valid_task(task_id)

    if request.method == "GET":
        return make_response(
            jsonify({"task":display_task(task)}), 200
        )

    elif request.method == "PUT":
        request_body = request.get_json()
        task.title = request_body["title"]
        task.description = request_body["description"]
        db.session.commit()

        return make_response(
            jsonify({"task":display_task(task)}), 200
        )

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()

        return make_response(
            jsonify(details=f"Task {task.task_id} \"{task.title}\" successfully deleted"), 200
        )

def valid_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"msg":f"Task id {task_id} invalid"}, 400))

    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"msg":f"Task id {task_id} not found"}, 404))

    return task

def display_task(task):
    return {
        "id" : task.task_id,
        "title" : task.title,
        "description" : task.description,
        "is_complete" : False if not task.completed_at else True
    }