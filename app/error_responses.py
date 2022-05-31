from __future__ import annotations
from typing import Any, Optional
from flask import make_response, jsonify, Response

# Error classes used to trigger specific error responses
class MissingValueError(Exception):
    def __init__(self):
        self.response = {"details": "Invalid data"}
        self.status = 400

class FormatError(ValueError):
    def __init__(self):
        self.response = ("Input value for attribute of task was invalid:"
                        " Value of completed_at must be str, datetime, or None. If"
                        " provided as a string, the timestamp must be in a standard"
                        " date and time format.")
        self.status = 400

class DBLookupError(LookupError):
    def __init__(self, target_cls: Any, target_id: int, detail: str = ''):
        self.response = (f"A {target_cls.__name__.lower()} with"
                        f" id of {target_id} was not found.{detail}")
        self.status = 404

class IDTypeError(TypeError):
    def __init__(self, target_id: Any, detail: str = ''):            
        self.response = f"{target_id} is not a valid id.{detail}"
        self.status = 400

def make_error_response(err: Exception, target_cls: Optional[Any] = None, 
                        detail: str = '') -> Response:
    '''Constructs error response based on Exception type.
    
    If supplied, 'detail' string is appended to the body of the response.
    '''

    if isinstance(err, (MissingValueError, FormatError, DBLookupError, IDTypeError)):
        return make_response(jsonify(err.response), err.status)
    # This alternate return statement in use by slackbot interaction and unknown errs
    print(detail)
    return make_response(jsonify(f"An unexpected error occurred. Error type: "
                                f"{err}, Error context: {target_cls}."
                                f"{detail}"), 500)
