from flask import jsonify, abort, make_response


def make_model_safely(cls, data_dict):
    try:
        model = cls.from_dict(data_dict)
    except KeyError:
        error_msg(f"Invalid data", 400)

    return model


def replace_model_safely(model, data_dict):
    try:
        model.replace_details(data_dict)
    except KeyError as err:
        error_msg(f"Missing key: {err}", 400)

# Ansel's Comments on creating a custom Python context manager
    with MissingKeyHandler():
        model.replace_details(data_dict)


def get_model_by_id(cls, id):
    try:
        id = int(id)
    except ValueError:
        error_msg(f"Invalid id: {id}", 400)

    model = cls.query.get(id)
    if model:
        return model

    error_msg(f"No {cls.__name__} data with id: {id}", 404)


def error_msg(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))


def success_msg(message, status_code):
    return make_response(jsonify(dict(details=message)), status_code)
