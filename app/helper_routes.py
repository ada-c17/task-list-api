from flask import jsonify, abort, make_response


def get_record_by_id(cls, id):
    try:
        id = int(id)
    except ValueError:
        # error_message(f"Invalid id {id}", 400)
        return make_response(jsonify(dict(details="Invalid data")), 400)

    model = cls.query.get(id)
    if model:
        return model