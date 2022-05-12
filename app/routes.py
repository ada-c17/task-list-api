# from flask import Blueprint, jsonify, request, abort, make_response
# from app.models.task import Task
# from app.models.goal import Goal
# from app import db
# from sqlalchemy import desc, asc
# from datetime import datetime 
# import requests
# import os

# #------task--------#

# tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# @tasks_bp.route("", methods=["POST"])
# def create_one_task():
#     request_body = request.get_json()

#     try:
#         new_task = Task(
#             title=request_body["title"],
#             description=request_body["description"])
#         new_task.title = request_body["title"]
#         new_task.description = request_body["description"]
        
#     except KeyError:
#         return {
#             "details": "Invalid data"
#         } , 400

#     if "completed_at" in request_body:
#         new_task.completed_at = request_body["completed_at"]

#     db.session.add(new_task)
#     db.session.commit()
    
#     response = jsonify({"task": {
#         "id": new_task.task_id,
#                 "title": new_task.title,
#                 "description": new_task.description,
#                 "is_complete": bool(new_task.completed_at)}
#     })
#     return response, 201

# @tasks_bp.route("", methods=["GET"])
# def get_all_tasks():
#     params = request.args
#     if "sort" in params :
#         if params["sort"] == "desc":
#             tasks = Task.query.order_by(desc(Task.title)).all()
#         else:
#             tasks = Task.query.order_by(asc(Task.title)).all()
#     else:
#         tasks = Task.query.all()

#     tasks_response = []
#     for task in tasks:
#         tasks_response.append(
#             {
#                 "id": task.task_id,
#                 "title": task.title,
#                 "description": task.description,
#                 "is_complete": bool(task.completed_at)
#             }
#         )
#     return jsonify(tasks_response), 200

# # helper function on testing valid tasks 
# def validate_task(task_id):
#     try:
#         task_id = int(task_id)
#     except ValueError:
#         response = {"details": f"Invalid id: {task_id}"}
#         abort(make_response(jsonify(response),400))
#     chosen_task = Task.query.get(task_id)

#     if chosen_task is None:
#         response = {"details": f"Could not find task with id #{task_id}"}
#         abort(make_response(jsonify(response),404))
#     return chosen_task

# @tasks_bp.route("/<task_id>", methods=["GET"])
# def get_one_task(task_id):
#     chosen_task = validate_task(task_id)
#     response = {"task": {
#             "id": chosen_task.task_id,
#             "title": chosen_task.title,
#             "description": chosen_task.description,
#             "is_complete": bool(chosen_task.completed_at)}
#         }
#     if chosen_task.goal_id:
#         response["task"].update({"goal_id": chosen_task.goal_id})
        

#     return jsonify(response), 200

# @tasks_bp.route("/<task_id>", methods=["PUT"])
# def replace_task(task_id):
#     chosen_task = validate_task(task_id)
#     request_body = request.get_json()

#     try:
#         chosen_task.title = request_body["title"]
#         chosen_task.description = request_body["description"]
        
    
#     except KeyError:
#         return {
#             "details": "title, description are required"
#         } , 400

#     try:
#         chosen_task.completed_at = request_body["completed_at"]

#     except KeyError:
#         pass

#     db.session.commit()
#     response = jsonify({"task": {
#         "id": chosen_task.task_id,
#                 "title": chosen_task.title,
#                 "description": chosen_task.description,
#                 "is_complete": bool(chosen_task.completed_at)}
#     })
#     return response, 200

# token = os.environ.get("SLACK_TOKEN")
# def send_slack_notifications(chosen_task):
#     #have info be able to send to slack channel
#     #make a post request from our routes to slack
#     slack_post_message = "https://slack.com/api/chat.postMessage"
#     headers = {"Authorization": f"Bearer {token}"} 
#     data = {
#         "channel": "task-notifications",
#         "text": f"Someone just completed the task {chosen_task.title}"

#     }
#     requests.post(slack_post_message, headers=headers, params=data)


# @tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
# def mark_complete_task(task_id):
#     chosen_task = validate_task(task_id)

#     chosen_task.completed_at = datetime.utcnow()

#     db.session.commit()

#     send_slack_notifications(chosen_task)

#     response = jsonify({"task": {
#         "id": chosen_task.task_id,
#         "title": chosen_task.title,
#         "description": chosen_task.description,
#         "is_complete": bool(chosen_task.completed_at)}
#     })

#     return response, 200

    
# @tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
# def mark_incomplete_task(task_id):
#     chosen_task = validate_task(task_id)

#     chosen_task.completed_at = None

#     print (chosen_task)

#     db.session.commit()
#     response = jsonify({"task": {
#         "id": chosen_task.task_id,
#                 "title": chosen_task.title,
#                 "description": chosen_task.description,
#                 "is_complete": bool(chosen_task.completed_at)}
#     })

#     return response, 200



# @tasks_bp.route("/<task_id>", methods = ["DELETE"])
# def delete_task(task_id):
#     chosen_task = validate_task(task_id)
#     db.session.delete(chosen_task)
#     db.session.commit()

#     return {
#         "details": f'Task {chosen_task.task_id} "{chosen_task.title}" successfully deleted'
#     }, 200


# #------goal------#

# goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

# @goals_bp.route("", methods=["POST"])
# def create_one_goal():
#     request_body = request.get_json()

#     try:
#         new_goal = Goal(title=request_body["title"])
#         new_goal.title = request_body["title"]
    
        
#     except KeyError:
#         return {
#             "details": "Invalid data"
#         } , 400

#     if "completed_at" in request_body:
#         new_goal.completed_at = request_body["completed_at"]

#     db.session.add(new_goal)
#     db.session.commit()
    
#     response = jsonify({"goal": {
#         "id": new_goal.goal_id,
#         "title": new_goal.title,}
#     })
#     return response, 201

# @goals_bp.route("", methods=["GET"])
# def get_all_goals():
#     goals = Goal.query.all()

#     goals_response = []
#     for goal in goals:
#         goals_response.append(
#             {
#                 "id": goal.goal_id,
#                 "title": goal.title,
#             }
#         )
#     return jsonify(goals_response), 200

# # helper function on testing valid goals
# def validate_goal(goal_id):
#     try:
#         goal = int(goal_id)
#     except ValueError:
#         response = {"details": f"Invalid id: {goal_id}"}
#         abort(make_response(jsonify(response),400))
#     chosen_goal = Goal.query.get(goal_id)

#     if chosen_goal is None:
#         response = {"details": f"Could not find goal with id #{goal_id}"}
#         abort(make_response(jsonify(response),404))
#     return chosen_goal


# @goals_bp.route("/<goal_id>", methods=["GET"])
# def get_one_goal(goal_id):
#     chosen_goal = validate_goal(goal_id)
#     response = jsonify({"goal": {
#         "id": chosen_goal.goal_id,
#         "title": chosen_goal.title}
                
#     })
#     return response, 200    


# @goals_bp.route("/<goal_id>", methods=["PUT"])
# def replace_goal(goal_id):
#     chosen_goal = validate_goal(goal_id)
#     request_body = request.get_json()

#     try:
#         chosen_goal.title = request_body["title"]
        
#     except KeyError:
#         return {
#             "details": "title is required"
#         } , 400

#     db.session.commit()
#     response = jsonify({"goal": {
#         "id": chosen_goal.goal_id,
#         "title": chosen_goal.title,}
#     })
#     return response, 200


# @goals_bp.route("/<goal_id>", methods = ["DELETE"])
# def delete_goal(goal_id):
#     chosen_goal = validate_goal(goal_id)
#     db.session.delete(chosen_goal)
#     db.session.commit()

#     return {
#         "details": f'Goal {chosen_goal.goal_id} "{chosen_goal.title}" successfully deleted'
#     }, 200


# @goals_bp.route("/<goal_id>/tasks", methods=["POST"])
# def send_task_list(goal_id):
#     chosen_goal = validate_goal(goal_id)
#     request_body = request.get_json()

#     chosen_tasks = []

#     for task_id in request_body["task_ids"]:
#         chosen_task = validate_task(task_id)
#         if chosen_task:
#             chosen_tasks.append(chosen_task)
    
#     chosen_goal.tasks = chosen_tasks

#     db.session.commit()
#     response = jsonify({
#         "id": chosen_goal.goal_id,
#         "task_ids": request_body["task_ids"]
#     })
#     return response, 200


# @goals_bp.route("/<goal_id>/tasks", methods=["GET"])
# def get_tasks_of_one_goal(goal_id):
#     chosen_goal = validate_goal(goal_id)
#     response = {
#         "id": chosen_goal.goal_id,
#         "title": chosen_goal.title,
#         "tasks": []

#     }
#     for task in chosen_goal.tasks:
#         response["tasks"].append({
#             "id": task.task_id,
#             "goal_id": chosen_goal.goal_id,
#             "title": task.title,
#             "description": task.description,
#             "is_complete": bool(task.completed_at)
#         })

#     return jsonify(response), 200
    
