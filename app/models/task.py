from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship('Goal', back_populates='tasks')

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