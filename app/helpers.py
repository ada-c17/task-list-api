# from flask import Blueprint, jsonify, make_response, abort, request
# from app.models.task import Task

# def validate_task(task_id):
#     try:
#         task_id = int(task_id)
#     except:
#         return abort(make_response({"message": f"Task {task_id} is invalid"}, 400))
#     task= Task.query.get(task_id)

#     if not task:
#         return abort(make_response({"message": f"Task {task_id} is not found"}, 404))

#     return task

# Invalid Task With Missing Data
# def validate_missing_data():
#     try:
#         task_id = int(task_id)
#     except:
#         return abort(make_response({"message": f"Task {task_id} is invalid"}, 400))
#     task= Task.query.get(task_id)

#     if not task:
#         return abort(make_response({"message": f"Task {task_id} is not found"}, 404))

#     return task