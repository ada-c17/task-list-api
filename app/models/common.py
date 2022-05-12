######################################################
# extension of JSONEncoder class for Task List objects
from flask.json import JSONEncoder

class TaskListJSONEncoder(JSONEncoder):

    def default(self, obj):
        if type(obj).__name__ == 'Task':
            details = {
                'id': obj.task_id,
                'title': obj.title,
                'description': obj.description,
                'is_complete': obj.completed_at != None
            }
            if obj.goal_id:
                details['goal_id'] = obj.goal_id
            return details
        elif type(obj).__name__ == 'Goal':
            return {
                'id': obj.goal_id,
                'title': obj.title
            }
        elif type(obj).__name__ == 'TasksGoal':
            return {
                'id': obj._.goal_id,
                'title': obj._.title,
                'tasks': obj._.tasks
            }
        return JSONEncoder.default(self, obj)

#########################################
# Shared validation and filtering methods

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
    if sort_style not in {None, 'asc', 'desc'}:
        sort_style = None
    if sort_style and len(params) == 0: # just sort
        return cls.query.order_by(getattr(cls.title,sort_style)()).all()
    
    # make query filters from these 3 params, ignoring any others
    filters = []
    if 'title' in params:
        filters.append(cls.title.like(f"%{params['title']}%"))
    if 'description' in params:
        filters.append(cls.description.like(f"%{params['description']}%"))
    if 'is_complete' in params:
        if not params['is_complete']:
            filters.append(cls.completed_at == None)
        filters.append(cls.completed_at != None)
    filters = tuple(filters)
    
    if not sort_style:
        return cls.query.filter(*filters).all()
    return (cls.query.filter_by(*filters)
                            .order_by(getattr(cls.title,sort_style)()).all())
