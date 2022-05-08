from flask import abort, make_response, jsonify

# Common model methods

def validate_id_by_model(cls, target_id):
    try:
        target_id = int(target_id)
    except:
        abort(make_response(jsonify(f"{target_id} is not a valid id."),400))
    target = cls.query.get(target_id)
    if not target:
        abort(make_response(jsonify(f"A {cls.__name__.lower()} with id of {target_id} was not found."),404))
    return target