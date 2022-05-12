from flask import abort, make_response

# validate
def validate(model, item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        abort(make_response({'msg': f"Invalid id: '{id}'. ID must be an integer"}, 400))
    
    item = model.query.get(item_id)

    if not item:
        abort(make_response({"message":f"item {item_id} not found"}, 404))
    
    return item

# get request body
