from flask import make_response, jsonify
from app.commons import MissingValueError, IDTypeError, DBLookupError, FormatError

def make_error_response(err, target_cls, target_id=None, detail=''):
    if isinstance(err, MissingValueError):
        return make_response(jsonify({"details": "Invalid data"}), 400)
    if isinstance(err, IDTypeError):
        return make_response(jsonify(f"{target_id} is not a valid id."
                                    f"{detail}"), 400)
    elif isinstance(err, DBLookupError):
        return make_response(jsonify(f"A {target_cls.__name__.lower()} with"
                                    f" id of {target_id} was not found."
                                    f"{detail}"), 404)
    elif isinstance(err, FormatError):
        detail = (" Value of completed_at must be str, datetime, or None. If"
                " provided as a string, the timestamp must be in a standard"
                " date and time format.")
        return make_response(jsonify(f"Input value for attribute of "
                                f"{target_cls.__name__.lower()} was "
                                f"invalid:{detail}"), 400)
    else:
        #TODO: Decide if a general error response is needed
        ...
