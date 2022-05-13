from flask import jsonify, make_response, abort

# helper function to generate error message
def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))