from flask import jsonify, abort, make_response

def get_record_by_id(cls, id):
    try:
        id = int(id)
    except ValueError:
        abort(make_response(jsonify({"message": f"Invalid id: {id} "}), 400))
    
    model = cls.query.get(id)

    if not model:
        abort(make_response(jsonify({"message": f"task {id} not found"}), 404))
    else: 
        return model