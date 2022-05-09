from flask import Blueprint, request, make_response, jsonify, abort
from app.models.goal import Goal
from app.models.task import Task
from app import db
from datetime import date
from app.helpers import valid_task, display_task, display_goal,post_slack_message

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

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
        
        if "completed_at" in request_body:
            task.completed_at = request_body["completed_at"]

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
            res.append(display_task(task))

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

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = valid_task(task_id)
    task.completed_at = date.today()
    db.session.commit()
    post_slack_message(f"Someone just completed the task {task.title}")

    return make_response(
            jsonify({"task":display_task(task)}), 200
        )

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = valid_task(task_id)
    if task.completed_at:
        task.completed_at = None
        db.session.commit()

    return make_response(
            jsonify({"task":display_task(task)}), 200
        )

@goals_bp.route("", methods = ["POST","GET"])
def handle_goals():
    if request.method == "POST":
        request_body = request.get_json()
        try:
            goal = Goal(title = request_body["title"])
        except:
            abort(make_response({"details":"Invalid data"}, 400))
        
        db.session.add(goal)
        db.session.commit()

        return make_response(
            jsonify({"goal":display_goal(goal)}), 201
            )
    
    elif request.method == "GET":
        goals = Goal.query.all()
        res = []
        for goal in goals:
            res.append(display_goal(goal))
        return make_response(jsonify(res), 200)
        

@goals_bp.route("/<goal_id>", methods = ["GET", "PUT", "DELETE"])
def handle_goal():
    pass