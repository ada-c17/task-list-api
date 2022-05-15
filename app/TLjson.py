from __future__ import annotations
from typing import Any

########################################################
# extension of JSONEncoder class for Task List objects #
########################################################

from flask.json import JSONEncoder

class TaskListJSONEncoder(JSONEncoder):
    '''A JSONEncoder subclass for serializing Task and Goal objects.
    
    Extends the default encoder so that flask.jsonify can process objects of
    type Task and Goal. All other types are passed to the base JSONEncoder
    class.

    Also recognizes a TasksGoal type used for alternate representation of Goal 
    objects with their associated Task objects.
    '''

    def default(self, obj: Any) -> dict[str, Any] | str | Any:
        '''Specifies how Task and Goal types should be represented in JSON.'''
        
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