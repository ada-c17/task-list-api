from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)

    def get_dict(self):
        is_complete = False
        if self.completed_at:
            is_complete = True
        
        response_dict =  {
            'id': self.task_id,
            'title': self.title,
            'description': self.description,
            'is_complete': is_complete
            }
        
        if self.goal_id:
            response_dict['goal_id'] = self.goal_id

        return response_dict