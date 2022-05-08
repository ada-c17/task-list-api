from app import db
from .common import validate_id_by_model


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)

    def to_json(self):
        details = {
                'id': self.task_id,
                'title': self.title,
                'description': self.description,
                'is_complete': self.completed_at != None
            }
        if self.goal_id:
            details['goal_id'] = self.goal_id
        return details
    
    @classmethod
    def new_task(cls, task_details):
        # Validate and clean input
        if 'title' not in task_details or 'description' not in task_details:
            raise ValueError
        if 'completed_at' not in task_details:
            task_details['completed_at'] = None
        
        return cls(
            title = task_details['title'],
            description = task_details['description'],
            completed_at = task_details['completed_at']
        )
    
    @classmethod
    def get_filtered_and_sorted(cls, request_args):
        params = dict(request_args)  # Conversion to make args object mutable
        sort_style = params.pop('sort', None)
        # TODO: Check behavior of filter_by() when supplied parameter not in model
        if sort_style and len(params) > 0:
            tasks = [task.to_json() for task in 
                        Task.query.filter_by(**params)
                                .order_by(getattr(Task.title,sort_style)())]
        elif sort_style:
            tasks = [task.to_json() for task in 
                        Task.query.order_by(getattr(Task.title,sort_style)())]
        else:
            tasks = [task.to_json() for task in Task.query.filter_by(**params)]

        return tasks

    @classmethod
    def validate_id(cls, target_id):
        return validate_id_by_model(cls, target_id)
