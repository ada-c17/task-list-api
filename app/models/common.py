
# Common model methods

def validate_and_get_by_id(cls, target_id):
    try:
        target_id = int(target_id)
    except:
        raise ValueError
    target = cls.query.get(target_id)
    if not target:
        raise LookupError
    return target

def get_filtered_and_sorted(cls, request_args):
    params = dict(request_args)  # Conversion to make args object mutable
    sort_style = params.pop('sort', None)
    # TODO: Check behavior of filter_by() when supplied parameter not in model
    if sort_style and len(params) > 0:
        results = [item.to_json() for item in 
                    cls.query.filter_by(**params)
                            .order_by(getattr(cls.title,sort_style)())]
    elif sort_style:
        results = [item.to_json() for item in 
                    cls.query.order_by(getattr(cls.title,sort_style)())]
    else:
        results = [item.to_json() for item in cls.query.filter_by(**params)]

    return results