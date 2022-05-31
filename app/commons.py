from __future__ import annotations
from typing import Mapping, Type

###########################################
# Shared validation and filtering methods #
###########################################

from flask import abort
from app.error_responses import IDTypeError, DBLookupError, make_error_response
from app.models.goal import Goal # Goal and Task imports here
from app.models.task import Task # only for type annotations

def validate_and_get_by_id(cls: Type[Task | Goal], target_id: str | int, errmsg: str = '') -> Task | Goal:
    '''Validates search id and returns result of database query.'''

    try:
        target_id = int(target_id)
    except:
        abort(make_error_response(IDTypeError(target_id, errmsg)))
    target = cls.query.get(target_id)
    if not target:
        abort(make_error_response(DBLookupError(cls, target_id, errmsg)))
    return target


def get_filtered_and_sorted(cls: Type[Task | Goal], request_args: Mapping) -> list[Task | Goal]:
    '''Builds SQL query from request params. Returns the result of DB query.'''

    params = dict(request_args)  # Conversion to make request.args mutable
    sort_style = params.pop('sort', None)
    if sort_style not in {None, 'asc', 'desc'}:
        sort_style = None
    if sort_style and len(params) == 0: # just sort
        return cls.query.order_by(getattr(cls.title,sort_style)()).all()
    
    # make query filters from these 3 params, ignoring any others
    filters = []
    if 'title' in params:
        filters.append(cls.title.ilike(f"%{params['title']}%"))
    if 'description' in params:
        filters.append(cls.description.ilike(f"%{params['description']}%"))
    if 'is_complete' in params:
        if params['is_complete'] == 'False':
            filters.append(cls.completed_at == None)
        else:
            filters.append(cls.completed_at != None)
    filters = tuple(filters)
    
    if not sort_style:
        return cls.query.filter(*filters).all() # just filter
    return (cls.query.filter(*filters)
                            .order_by(getattr(cls.title,sort_style)()).all())
