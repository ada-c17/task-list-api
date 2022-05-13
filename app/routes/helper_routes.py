from flask import make_response, abort, jsonify
from app.models.task import Task
import datetime


def validate_id(cls, id):
        try:
            id = int(id)
        except ValueError:
            abort(make_response(jsonify(f"{cls.__name__} {id} is invalid"), 400))
        instance = cls.query.get(id)
        if not instance:
            abort(make_response(jsonify(f"{cls.__name__} {id} not found"), 404))
        return instance

def validate_request(request, *attributes):
    request_body = request.get_json()
    for attribute in attributes:
        try:
            request_body[attribute]
        except KeyError:
            abort(make_response({"details": "Invalid data"}, 400)) 
    return request_body

def get_filtered_tasks(request):
    title_param = request.args.get("title")
    description_param = request.args.get("description")
    is_complete_param = request.args.get("is_complete")
    sort_param = request.args.get("sort")

    tasks = Task.query

    if title_param:
        tasks = tasks.filter_by(title=title_param)
    if description_param:
        tasks = tasks.filter_by(description=description_param)
    if is_complete_param == "true":
        tasks = tasks.filter(Task.completed_at != None)
    elif is_complete_param == "false":
        tasks = tasks.filter_by(completed_at=None)
    if sort_param:    
        if sort_param == "asc":
            tasks = tasks.order_by(Task.title.asc())
        elif sort_param == "desc":
            tasks = tasks.order_by(Task.title.desc())

    tasks = tasks.all()
    return tasks

def validate_datetime(request_body):
    datetime_string = (
        request_body["completed_at"] if request_body.get("completed_at", None) != None else None
    )
    if datetime_string is None:
        return datetime_string

    try:
        format = "%a, %d %B %Y %H:%M:%S %Z" 
        dt = datetime.datetime.strptime(datetime_string, format)
        return dt
    except ValueError:
        abort(make_response({"details": "Invalid date format. Use YYYY-MM-DD HH:MM:SS."}, 400))
