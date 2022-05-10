from app.models.task import Task
from flask import abort, make_response,request

def validate_task(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"Task{id} is invalid"}, 400))

    task = Task.query.get(id)
    if not task:
        abort(make_response({"message": f"Task{id} not found"}, 404))

    
    return task

def validate_client_requests(request_body):
    try:
        new_task = Task.create(request_body)
    except KeyError:
        abort(make_response({"details": "Invalid data"},400))
    
    return new_task
    
    


#     try:
#         len(req) == 2
#     except TypeError:
#         abort(make_response({"details": "Invalid data"},400))
#     # if "description" not in req:
#     #     abort(make_response({"details": "Invalid data"},400))
#     req = req.get_json()

