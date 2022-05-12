from flask import abort, make_response


def get_or_abort(model, item_id):

    try:
        item_id = int(item_id)
    except:
        abort(make_response({"message": f"{model.__name__} {item_id} invalid."}, 400))

    item = model.query.get(item_id)

    if not item:
        abort(make_response({"message": f"{model.__name__} {item_id} not found."}, 404))

    return item


def get_JSON_request_body(request):

    if not request.is_json:
        abort(make_response({"message": "Missing JSON request body."}, 400))

    return request.get_json()
