from flask import abort, make_response


def handle_id_request(id, database):
    try:
        id = int(id)
    except:
        abort(make_response({"msg": f"Invalid {database.db_name} ID '{id}'."}, 400))

    query = database.query.get(id)

    if not query:
        abort(make_response({"msg": f"{database.db_name} ID '{id}' does not exist."}, 404))

    return query

def check_complete_request_body(request, database):
    request_body = request.get_json()
    if all(element in request_body for element in database.expected_elements):
        if all(type(request_body[element]) == database.expected_elements[element] \
                    for element in database.expected_elements):
                        return request_body
    abort(make_response({"details": "Invalid data"}, 400))