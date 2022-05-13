from flask import jsonify, abort, make_response

def validate_task(cls, id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"task {id} invalid"}, 400))

    model = cls.query.get(id)

    if not model:
        abort(make_response({"message":f"task {id} not found"}, 404))

    return model

def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))