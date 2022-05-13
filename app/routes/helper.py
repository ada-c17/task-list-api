from flask import jsonify, abort, make_response, request
from sqlalchemy import asc,desc
from app.models.goal import Goal
from app.models.task import Task

def validate_task(cls,task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return abort(make_response({"details":"Invalid data"},400))
    obj = cls.query.get(task_id)

    if not obj:
        if cls.__name__ == "Goal":
            return abort(make_response({"message":f"goal {task_id} not found"}, 404))
        if cls.__name__ == "Task":
            return abort(make_response({"message":f"task {task_id} not found"}, 404))
    return obj

def sort_filter_get(cls):
    sort_query = request.args.get("sort")
    title_query = request.args.get("title")

    if sort_query == "asc":
        obj = cls.query.order_by(asc(cls.title))
    elif sort_query == "desc":
        obj = cls.query.order_by(desc(cls.title))
    elif title_query:
        obj = cls.query.filter_by(cls.title)
    else:
        obj = cls.query.all()
    
    return obj

    

