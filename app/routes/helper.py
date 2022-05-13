# from turtle import title
from flask import abort, make_response, request


def validate_obj(cls,id):
    try:
        id = int(id)
    except ValueError:
        return abort(make_response({"details":"Invalid data"},400))
    obj = cls.query.get(id)

    if not obj:
        if cls.__name__ == "Goal":
            return abort(make_response({"message":f"goal {id} not found"}, 404))
        if cls.__name__ == "Task":
            return abort(make_response({"message":f"task {id} not found"}, 404))
    return obj

def sort_filter_get(cls):
    sort_query = request.args.get("sort")
    title_query = request.args.get("title")
    des_query = request.args.get("description")
    if sort_query == "asc":
        obj = cls.query.order_by(cls.title.asc())
    elif sort_query == "desc":
        obj = cls.query.order_by(cls.title.desc())
    elif title_query:
        obj = cls.query.filter_by(title = title_query)
    elif des_query:
        obj = cls.query.filter_by(description = des_query)    
    else:
        obj = cls.query.all()
    
    return obj



    

