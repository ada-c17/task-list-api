from flask import Blueprint, request, make_response, jsonify, abort
from app.models.goal import Goal
from app.models.task import Task
from app import db
from datetime import datetime
from app.helpers import valid_task, valid_goal, display_task, display_goal, post_slack_message, check_completed_at

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@tasks_bp.route("", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "POST":
        request_body = request.get_json()
        try:
            task = Task(
                title = request_body["title"],
                description = request_body["description"],
                completed_at = check_completed_at(request_body)
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
            res.append(display_task(task))

        return make_response(jsonify(res), 200)

@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(task_id):
    task = valid_task(task_id)

    if request.method == "GET":
        res = display_task(task)
        if task.goal_id:
            res["goal_id"] = task.goal_id 

        return make_response(
            jsonify({"task":res}), 200
        )

    elif request.method == "PUT":
        request_body = request.get_json()
        task.title = request_body["title"]
        task.description = request_body["description"]
        task.completed_at = check_completed_at(request_body)
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
    task.completed_at = datetime.utcnow()
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
def handle_goal(goal_id):
    goal = valid_goal(goal_id)

    if request.method == "GET":
        return make_response(
            jsonify({"goal":display_goal(goal)}), 200
        )

    elif request.method == "PUT":
        request_body = request.get_json()
        try:
            goal.title = request_body["title"]
        except:
            abort(make_response({"details":"Invalid data"}, 400))

        db.session.commit()

        return make_response(
            jsonify({"goal":display_goal(goal)}), 200
        )

    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        return make_response(
            jsonify({"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"}), 200
        )

@goals_bp.route("/<goal_id>/tasks", methods = ["POST", "GET"])
def handle_goal_tasks(goal_id):
    goal = valid_goal(goal_id)

    if request.method == "POST":
        request_body = request.get_json()
        for task_id in request_body["task_ids"]:
            task = valid_task(task_id)
            task.goal = goal

        db.session.commit()
            
        return jsonify({
                "id": goal.goal_id,
                "task_ids": [task.task_id for task in goal.tasks]
        }), 200
        
    if request.method == "GET":
        tasks = []
        for task in goal.tasks:
            task_str = display_task(task)
            task_str["goal_id"] = goal.goal_id
            tasks.append(task_str)

        return jsonify({
            "id":goal.goal_id,
            "title":goal.title,
            "tasks": tasks
        })
