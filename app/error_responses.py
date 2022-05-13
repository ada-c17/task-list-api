from flask import make_response, jsonify

class MissingValueError(Exception): ...
class FormatError(ValueError): ...
class DBLookupError(LookupError): ...
class IDTypeError(TypeError): ...

def make_error_response(err, target_cls, target_id=None, detail=''):
    ''''''
    if isinstance(err, MissingValueError):
        return make_response(jsonify({"details": "Invalid data"}), 400)
    if isinstance(err, IDTypeError):
        return make_response(jsonify(f"{target_id} is not a valid id."
                                    f"{detail}"), 400)
    if isinstance(err, DBLookupError):
        return make_response(jsonify(f"A {target_cls.__name__.lower()} with"
                                    f" id of {target_id} was not found."
                                    f"{detail}"), 404)
    if isinstance(err, FormatError):
        detail = (" Value of completed_at must be str, datetime, or None. If"
                " provided as a string, the timestamp must be in a standard"
                " date and time format.")
        return make_response(jsonify(f"Input value for attribute of "
                                f"{target_cls.__name__.lower()} was "
                                f"invalid:{detail}"), 400)
    # Currently this last return statement should never run, incl. for future
    return make_response(jsonify(f"An unexpected error occurred. Error type: "
                                f"{err}, Error context: {target_cls.__name__}."
                                f"{detail}"), 500)
