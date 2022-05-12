from flask import Blueprint,jsonify, request, make_response, abort
from app.models.goal import Goal
from app.models.task import Task
from app import db


goals_bp = Blueprint("goal", __name__,url_prefix="/goals")


# create a goal
@goals_bp.route('', methods=['POST'])
def create_one_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return jsonify({
            "details": "Invalid data"
        }), 400
    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    response = {
        "goal":{
        "id":new_goal.goal_id,
        "title":new_goal.title }
    }
    return jsonify(response), 201

# get all goals
@goals_bp.route('', methods=['GET'])
def get_all_goals():
    goals= Goal.query.all()

    goal_response = []
    for goal in goals:
        goal_response.append ({
        "id":goal.goal_id,
        "title":goal.title 
    })
    return jsonify(goal_response), 200


# validate goal
def validate_goal(goal_id):
    try:
        goal_id = int (goal_id)
    except ValueError:
        rsp =  {"msg": f"Invalid id:{goal_id}"}
        abort( make_response (jsonify(rsp), 400))
        
    chosen_goal = Goal.query.get(goal_id)

    if chosen_goal is None:
        abort( make_response({"massage": f" Goal {goal_id} not found"}, 404))
    
    return chosen_goal


# get one goal
@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    chosen_goal = validate_goal(goal_id)

    request_body = request.get_json()

    response = {
        "goal":{
        "id":chosen_goal.goal_id,
        "title":chosen_goal.title }
    }
    return jsonify(response), 200


# update one goal
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    chosen_goal = validate_goal(goal_id)

    request_body = request.get_json()

    try:
        chosen_goal.title = request_body["title"]

    except KeyError:
        return {
            "msg": "title is required"
        },404

    db.session.commit()

    response = {
        "goal":{
        "id":chosen_goal.goal_id,
        "title":chosen_goal.title }
    }
    return jsonify(response), 200


# delete one goal
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    chosen_goal = validate_goal(goal_id)

    db.session.delete(chosen_goal)
    db.session.commit()

    response_body = { 
        "details":f'Goal {chosen_goal.goal_id} "{chosen_goal.title}" successfully deleted'
    }

    return jsonify(response_body), 200


@goals_bp.route('/<goal_id>/tasks', methods=['POST'])
def create_tasks_for_one_goal(goal_id):
    goal = validate_goal(goal_id)
    # goal = Goal.query.get(goal_id)
    request_body = request.get_json()
   
    for task_id in request_body.get("task_ids"):
        tasks=Task.query.get(task_id)
        goal.tasks.append(tasks)

    db.session.commit()

    response = {
        "id":goal.goal_id,
        "task_ids":request_body.get("task_ids")
    }
    return jsonify(response), 200


@goals_bp.route('/<goal_id>/tasks', methods=['GET'])
def get_tasks_for_a_goal(goal_id):
    chosen_goal = validate_goal(goal_id)

    chosen_goal_tasks=[]
    for task in chosen_goal.tasks:
        chosen_goal_tasks.append(
            {
                "id":task.task_id,
                "goal_id":task.goal_id,
                'title':task.title,
                'description':task.description,
                'is_complete':bool(task.completed_at)
            }
        )

    response= {
        "id":chosen_goal.goal_id,
        "title":chosen_goal.title,
        # "task":chosen_goal_tasks["goal_id"],
        "tasks": chosen_goal_tasks
    }
    return jsonify(response), 200
