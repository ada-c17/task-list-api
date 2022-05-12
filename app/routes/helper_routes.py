from flask import make_response, abort, jsonify
from app.models.task import Task


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
