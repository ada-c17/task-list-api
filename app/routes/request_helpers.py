from flask import abort, make_response

def handle_id_request(id, database):
    '''
    Validate <id> from request route, return db.Model object

    Arguments:
        id: <id> from request route
        database: db_name class variable (see goal.py, task.py)
    '''
    try:
        id = int(id)
    except:
        abort(make_response({"msg": f"Invalid {database.db_name} ID '{id}'."}, 400))

    query = database.query.get(id)

    if not query:
        abort(make_response({"msg": f"{database.db_name} ID '{id}' does not exist."}, 404))

    return query

def check_complete_request_body(request, database):
    '''
    Validate request body, return request body json

    Arguments:
        request: request body object
        database: db_name class variable (see goal.py, task.py)
    '''
    request_body = request.get_json()
    #use expected_elements class variable to validate complete request body 
    #for base POST, PUT routes 
    if all(element in request_body for element in database.expected_elements):
        if all(type(request_body[element]) == database.expected_elements[element] \
                    for element in database.expected_elements):
                        return request_body
    abort(make_response({"details": "Invalid data"}, 400))