from flask import abort, make_response, jsonify

# Decorators to implement common model methods

def define_validation_on_model(func):

    def inner(cls, target_id):
        try:
            target_id = int(target_id)
        except:
            abort(make_response(jsonify(f"{target_id} is not a valid id."),400))
        target = cls.query.get(target_id)
        if not target:
            abort(make_response(jsonify(f"A {cls.__name__.lower()} with id of {target_id} was not found."),404))
        return target
    
    return inner