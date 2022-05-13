
from app.models.task import Task
from app.models.goal import Goal
from app import db
from flask import Blueprint, jsonify,abort,make_response,request
from sqlalchemy.sql.functions import now
import os
import requests


task_list_bp = Blueprint("task_list", __name__,url_prefix="/tasks")
goal_list_bp = Blueprint("goal_list", __name__,url_prefix="/goals")


def validate_task(task_id):
    try:
       task_id = int(task_id)
    except:
        abort(make_response({"message":f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"task {task_id} not found"}, 404))

    return task




#Get tasks sorted or get all tasks
@task_list_bp.route("", methods=["GET"])
def get_tasks_sorted():
   
    sort_query = request.args.get("sort")

   
    if sort_query and sort_query=="asc":
        tasks= Task.query.order_by(Task.title.asc())
    elif sort_query and sort_query=="desc":
        tasks= Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()


        
    task_response = []
    for task in tasks:
        task_response.append(task.to_json())
    return make_response( jsonify(task_response),200)




#Get one task
@task_list_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
   
    task = Task.query.get(task_id)

    if task:
        return {
            "task": task.to_json()
        }
    else:
        return make_response(jsonify(None), 404)



#Create one task
@task_list_bp.route("", methods=["POST"])
def create_new_task():
   
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body:
             return make_response({"details":f"Invalid data"}, 400)

        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        )
        if "completed_at" in request_body:
            new_task.completed_at = request_body["completed_at"]
        

        db.session.add(new_task)
        db.session.commit()
        
        return jsonify({"task":new_task.to_json()}),201



#Update one task
@task_list_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return jsonify({"task":task.to_json()}),200


#Delete one task
@task_list_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details":f'Task {task.task_id} \"{task.title}\" successfully deleted'}),200
    



#Mark complete for one task and use Slack API
@task_list_bp.route('/<task_id>/mark_complete', methods=['PATCH'])
def mark_complete(task_id):
    task=Task.query.get(task_id)
    if not task:
        abort(make_response({"message":f"task {task_id} not found"}, 404))
    task.completed_at = now()
    db.session.add(task)
    db.session.commit()
    

    slack_api_url = "https://slack.com/api/chat.postMessage"
    params = {
        "channel" : "test-channel",
        "text" : f"Someone just completed the task {task.title}"
    }
    headers = {
        "Authorization" : f"Bearer {os.environ.get('SLACK_API_HEADER')}"
    }
    requests.get(url=slack_api_url, params=params, headers=headers)
    
    return make_response(jsonify({"task" : task.to_json()}))


#Mark incomplete for one task
@task_list_bp.route('/<task_id>/mark_incomplete', methods=['PATCH'])
def mark_incomplete(task_id):
    task=Task.query.get(task_id)
    if not task:
        abort(make_response({"message":f"task {task_id} not found"}, 404))
    task.completed_at = None
    db.session.add(task)
    db.session.commit()
    task_response={"task":{
            "id": task.task_id,
            "title": task.title,
            "description": task.description, "is_complete": False
        }}
    return jsonify(task_response),200

#*******************************Goal_routes*******************************************

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message":f"goal {goal_id} invalid"}, 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message":f"goal {goal_id} not found"}, 404))

    return goal


#Create one goal
@goal_list_bp.route("", methods=["post"])
def create_new_goal():
   
        request_body = request.get_json()
        if "title" not in request_body:
            return {
        "details": "Invalid data"
    },400
        new_goal = Goal(title=request_body["title"],
                        )


        db.session.add(new_goal)
        db.session.commit()

        return {"goal":{"id":new_goal.goal_id, "title":new_goal.title}},201



#Get one goal
@goal_list_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)

    return{"goal": {
        "id": goal.goal_id,
        "title": goal.title,
        }}


#Get all goals
@goal_list_bp.route("", methods=["GET"])
def get_all_goal():
    goals = Goal.query.all()
        
    goal_response = []
    for goal in goals:
        goal_response.append({
            "id": goal.goal_id,
            "title": goal.title,
            
        })
    return jsonify(goal_response),200


#Update one goal
@goal_list_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]
    goal.decription = request_body["description"]
    

    db.session.commit()

    return make_response(jsonify(f"goal #{goal.goal_id} successfully updated")),200


#Delete one goal
@goal_list_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details":f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}


#********************************Nested routes************************************

#Show tasks for a goal
@goal_list_bp.route("/<goal_id>/tasks", methods=["GET"])
def show_tasks_for_a_goal(goal_id):
    goal = validate_goal(goal_id)
    tasks = Task.query.filter_by(goal=goal)
    task_list = []

    for task in tasks:
        task_list.append(task.to_json())
    return make_response(jsonify({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": task_list
    }), 200)


#Post tasks to a goal
@goal_list_bp.route("/<goal_id>/tasks", methods=["POST"])
def posts_tasks_to_a_goal(goal_id):
    goal = validate_goal(goal_id)
    


    request_body = request.get_json()
    for task_id in request_body["task_ids"]:
        task = Task.query.get(task_id)

        task.goal_id=goal.goal_id
    if not task:
        abort(make_response({"message":f"task {task_id} invalid"}, 400))
    

    goal.tasks.append(task)
    db.session.commit()
    
    return make_response(jsonify({"id":goal.goal_id,"task_ids":request_body["task_ids"]}),200)
