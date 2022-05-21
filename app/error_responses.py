from __future__ import annotations
from typing import Any, Optional
from flask import make_response, jsonify, Response

# Error classes used to trigger specific error responses
class MissingValueError(Exception): ...
class FormatError(ValueError): ...
class DBLookupError(LookupError): ...
class IDTypeError(TypeError): ...

def make_error_response(err: Exception, target_cls: Any | None, 
                        target_id: Optional[str | int] = None, 
                        detail: str = '') -> Response:
    '''Constructs error response based on Exception type.
    
    If supplied, 'detail' string is appended to the body of the response.
    '''

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
    # Currently this last return statement should never run: for future use
    print(detail)
    return make_response(jsonify(f"An unexpected error occurred. Error type: "
                                f"{err}, Error context: {target_cls}."
                                f"{detail}"), 500)
