from flask import abort, make_response, jsonify
from app.models.goal import Goal

# def check_task_exists(task_id):
#     task = Task.query.get(task_id)

#     if not task:
#         abort(make_response(jsonify({"error": f"Task {task_id} does not exist"}), 404))
    
#     return task

def try_to_make_goal(response_body):
    try:
        return Goal.make_goal(response_body)
    except KeyError:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))


