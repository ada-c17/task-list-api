# from flask import Blueprint, jsonify, make_response, request
# from app import db
# from app.models.goal import Goal
# # from .helpers import send_slack_completed_message, validate_task

# goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# @goals_bp.route("", methods=["POST"])
# def create_goal():
#     request_body = request.get_json()

#     new_task = Task.from_json(request_body)

#     db.session.add(new_task)
#     db.session.commit()

#     return jsonify({"task":new_task.to_json()}), 201


# @goals_bp.route("", methods=["GET"])
# def read_tasks():
#     sorting_pattern = request.args.get("sort")
    
#     if sorting_pattern == "asc":
#         tasks = Task.query.order_by(Task.title.asc()).all()
#     elif sorting_pattern == 'desc':
#         tasks = Task.query.order_by(Task.title.desc()).all()
#     elif not sorting_pattern:
#         tasks = Task.query.all()

#     tasks_response = [task.to_json() for task in tasks]
#     print(tasks_response)
        
#     return jsonify(tasks_response), 200


# @goals_bp.route("/<task_id>", methods=["GET"])
# def get_one_task(task_id):
#     task = validate_task(task_id)
#     return jsonify({'task':task.to_json()}), 200


# @goals_bp.route("/<task_id>", methods=["PUT"])
# def update_one_task(task_id):
#     task = validate_task(task_id)
#     request_body = request.get_json()

#     task.update_task(request_body)

#     db.session.commit()

#     return jsonify({'task':task.to_json()}), 200


# @goals_bp.route("/<task_id>", methods=["DELETE"])
# def delete_task(task_id):
#     task = validate_task(task_id)
#     db.session.delete(task)
#     db.session.commit()

#     return jsonify({"details":f'Task {task_id} "{task.title}" successfully deleted'} ), 200


# @goals_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
# def mark_task_complete(task_id):

#     task = validate_task(task_id) 
    
#     task.completed_at = date.today()

#     db.session.commit()
    
#     send_slack_completed_message(task)

#     return jsonify ({'task': task.to_json()}), 200


# @goals_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
# def mark_task_incomplete(task_id):
#     task = validate_task(task_id)
    
#     task.completed_at = None

#     db.session.commit()

#     return jsonify({"task":task.to_json()}), 200
        



