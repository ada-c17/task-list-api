from flask import make_response, jsonify

def make_error_response(err, target_cls, target_id, detail=''):
    if isinstance(err, ValueError):
        return make_response(jsonify(f"{target_id} is not a valid id."
                                    f"{detail}"), 400)
    elif isinstance(err, LookupError):
        return make_response(jsonify(f"A {target_cls.__name__.lower()} with "
                                    f"id of {target_id} was not found."
                                    f"{detail}"), 404)
    elif isinstance(err, TypeError):
        return make_response(jsonify(f"Input value for attribute of "
                                    f"{target_cls.__name__.lower()} was "
                                    f"invalid:{detail}"), 400)
    else:
        #TODO: Decide if a general error response is needed
        ...