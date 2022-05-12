from flask import Blueprint, request, jsonify, make_response, abort
from app.models.goal import Goal
from .models.task import Task
from app import db

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

"""Wave05"""
@goal_bp.route("", methods=["POST"])
def create_goals():
    resquest_body = request.get_json()
    
    if "title" in resquest_body:
        goal = Goal(title=resquest_body["title"])
    else:
        return {"details": "Invalid data"}, 400
    
    db.session.add(goal)
    db.session.commit()
    
    return {
        "goal":
            {
            "id": goal.goal_id,
            "title": goal.title
            }
    }, 201
    
@goal_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    response_body = []
    for goal in goals:
        response_body.append(goal.to_json())
    
    return jsonify(response_body), 200


def goal_id_validation(input_id):
    try:
        input_id = int(input_id)
    except ValueError:
        rsp = {"msg": f"Invalid goal id #{input_id}."}
        abort(make_response(jsonify(rsp), 400))
    
    valid_id = Goal.query.get(input_id)
     
    if valid_id is None:
        rsp = {"msg": f"Given goal #{input_id} is not found."}
        #raise ValueError({"msg": f"Given task #{taskID} is not found."})
        abort(make_response(jsonify(rsp), 404))

    return valid_id

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = goal_id_validation(goal_id)
    
    return jsonify({
         "goal": goal.to_json()}), 200

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = goal_id_validation(goal_id)
    request_body = request.get_json()
    
    if request_body and "title" in request_body:
        goal.title = request_body["title"]
    db.session.commit()
    
    return jsonify({
        "goal": goal.to_json()
    }), 200
    
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = goal_id_validation(goal_id)
    goals = Goal.query.all()
    
    # if len(goals) < 1:
    #     abort(make_response({"msg": "Not Found"}), 404)
        
    db.session.delete(goal)
    db.session.commit()
    
    return {
        "details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
    }, 200
    
@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_tasks_for_one_goal(goal_id):
    goal = goal_id_validation(goal_id)
    goal = Goal.query.get(goal_id) 
    #goal.tasks [] empty at this point
    
    request_body = request.get_json()
    #"task_ids": [1, 2, 3]
    #each Goal has (zero)one or many tasks[]
    for task_id in request_body.get("task_ids"):
        #build relationship between goal and task here
        task = Task.query.get(task_id)
        goal.tasks.append(task)
 
    db.session.commit()
    #goal.tasks = [<Task1>, <Task 2>, <Task 3>]
    
    return jsonify({
        "id": task.goal_id,
        "task_ids": request_body.get("task_ids")
    }), 200
"""
database visualization
 task_id |       title        |           description            |        completed_at        | goal_id 
---------+--------------------+----------------------------------+----------------------------+---------
       3 | A Brand New Task   | Test Description                 |                            |        
       6 | A Brand New Task   | Test Description                 |                            |        
       7 | A Brand New Task   | Test Description                 |                            |        
       9 | A Brand New Task   | Test Description                 |                            |        
      10 | A Brand New Task   | Test Description                 |                            |        
      12 | Coding flask       | Due next Friday                  |                            |        
      13 | Capstone Project   | Build full stack web application |                            |        
      11 | Updated Task Title | Updated Test Description         | 2022-05-07 03:21:52.90605  |        
       4 | A Brand New Task   | Test Description                 | 2022-05-07 20:51:40.542297 |        
       5 | A Brand New Task   | Test Description                 | 2022-05-07 20:51:58.383394 |        
       2 | A Brand New Task   | Test Description                 | 2022-05-07 21:05:26.080884 |        
       8 | A Brand New Task   | Test Description                 | 2022-05-08 21:03:25.409507 |        

 goal_id |                title                 
---------+--------------------------------------
       1 | Build a habit of going outside daily
       2 | Build a habit of sleeping at 11 pm
       3 | Build a habit of getting up at 7 am
"""


@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_one_goal(goal_id):
    goal = goal_id_validation(goal_id)

    return make_response(jsonify(goal.to_json2()), 200)
