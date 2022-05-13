from flask import jsonify, abort, make_response

def get_or_abort(model, id):
    try:
        id = int(id)
    except ValueError:
        rsp = {"msg": f"Invalid id: {id}"}
        abort(make_response(jsonify(rsp), 400))
    chosen_model = model.query.get(id)
    if chosen_model is None:
        rsp = {"msg": f"Could not find id {id}"}
        abort(make_response(jsonify(rsp), 404))
    return chosen_model