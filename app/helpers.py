from flask import abort, make_response, jsonify
from app.models.task import Task


def validate_object(cls, id):
    try:
        id = int(id)
    except:
        return abort(make_response(jsonify(f"{cls.__name__} {id} is invalid"), 400))

    obj = cls.query.get(id)

    if not obj:
        return abort(make_response(jsonify(f"{cls.__name__} {id} does not exist"), 404))
    return obj

# create helper function for invalid data in create


# def validate_new_data(cls, request_body):
#     try:
#         new_data = cls.create(request_body)
#         db.session.add(new_data)
#         db.session.commit()
#     except KeyError:
#         return abort(make_response(jsonify({"details": "Invalid data"}), 400))
#     return new_data.to_json(), 201

#     new_goal = Goal.create(request_body)
