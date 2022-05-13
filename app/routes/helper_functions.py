from flask import jsonify, abort, make_response

# Helper functions

def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

def get_record_by_id(id, model):
    try: 
        id = int(id)
    except ValueError:
        error_message(f"Invalid {model.__name__.lower()} id {id}", 400)
    
    record = model.query.get(id)

    if record:
        return record
    
    error_message(f"No {model.__name__.lower()} with id {id} found", 404)