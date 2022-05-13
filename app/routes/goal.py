from flask import Blueprint, request,jsonify
from app.models.goal import Goal 
from app.models.task import Task 
from app import db 
from sqlalchemy import desc, asc

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return {"details": "Invalid data"}, 400
    
    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return {
        "goal": new_goal.to_json()
    }, 201


@goals_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()

    params = request.args 
    if "sort" in params:
        sort = params["sort"]
        if sort.lower() == "asc": # note default is asc, but included to be more explicit
            goals = Goal.query.order_by(asc(Goal.title)).all()
        elif sort.lower() == "desc":
            goals = Goal.query.order_by(desc(Goal.title)).all()
    else:    
        goals = Goal.query.all()

    # before refactoring
    # goals_response = []
    # for goal in goals:
    #     goals_response.append(goal.to_json())

    goals_response = [goal.to_json() for goal in goals]
    
    return jsonify(goals_response), 200
    

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal(goal_id):
    goal = Goal.validate_goal(goal_id)

    return {
        "goal": goal.to_json()
    }, 200


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = Goal.validate_goal(goal_id)
    request_body = request.get_json()

    if "title" not in request_body:
        return {"details": "Invalid data"}, 400
    else:
        goal.title = request_body["title"]
    
    db.session.commit()

    return {
        "goal": goal.to_json()
    }, 200


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = Goal.validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {
        "details": f'Goal {goal_id} "{goal.title}" successfully deleted'
    }, 200


@goals_bp.route("/<goal_id>/tasks", methods = ["POST"])
def create_tasks_for_goal(goal_id):
    goal = Goal.validate_goal(goal_id)
    request_body = request.get_json()

    if "task_ids" in request_body:
        tasks = request_body["task_ids"]

    retrieved_tasks = [Task.validate_task(task) for task in tasks if task]

    # before refactoring
    # retrieved_tasks = []

    # for task in tasks:
    #     task = Task.validate_task(task)
    #     if task:
    #         retrieved_tasks.append(task)
    
    goal.tasks = retrieved_tasks
    db.session.commit()
        
    return {
        "id": goal.goal_id,
        "task_ids": tasks 
    }, 200


@goals_bp.route("/<goal_id>/tasks", methods = ["GET"])
def get_tasks_for_goal(goal_id):
    goal = Goal.validate_goal(goal_id)
    tasks = goal.tasks 

    # before refactoring
    # tasks_response = []

    # for task in tasks:
    #     tasks_response.append({
    #         "id": task.task_id, 
    #         "goal_id": task.goal_id,
    #         "title": task.title, 
    #         "description": task.description, 
    #         "is_complete": task.is_complete()
    #     })

    # goal.tasks = tasks_response
    
    # return {
    #     "id": goal.goal_id,
    #     "title": goal.title,
    #     "tasks": tasks_response
    # }, 200

    tasks_response = [task.to_json() for task in tasks]

    goal = goal.to_json()
    goal["tasks"] = tasks_response
    return goal, 200

