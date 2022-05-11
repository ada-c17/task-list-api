from flask import make_response, jsonify

def make_error_response(err, target_cls, target_id, detail=''):
    if isinstance(err, ValueError):
        return make_response(jsonify(f"{target_id} is not a valid id.{detail}"), 400)
    elif isinstance(err, LookupError):
        return make_response(jsonify(f"A {target_cls.__name__.lower()} with "
                                    f"id of {target_id} was not found.{detail}"), 404)
    else:
        #TODO: Decide if a general error response is needed
        ...