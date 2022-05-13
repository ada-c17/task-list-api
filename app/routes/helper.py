from flask import jsonify, abort, make_response, request
from sqlalchemy import asc,desc

def validate_task(cls,task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return abort(make_response({"details":"Invalid data"},400))
    obj = cls.query.get(task_id)

    if not obj:
        return abort(make_response({"message":f"task {task_id} not found"}, 404))
    return obj

def sort_or_get(cls):
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        obj = cls.query.order_by(asc(cls.title))
    elif sort_query == "desc":
        obj = cls.query.order_by(desc(cls.title))
    else:
        obj = cls.query.all()
    
    return obj

