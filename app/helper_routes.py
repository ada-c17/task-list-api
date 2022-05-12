
from flask import jsonify, abort, make_response

def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))




# validate record
# pass in the actual class in our function, to use for both models ! 