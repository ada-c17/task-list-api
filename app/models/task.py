from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_value = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    
    def dict(self):
        return (dict(task={
            "id" : self.task_id,
            "title": self.title,
            "description" : self.description,
            "is_complete" : bool(self.completed_at),
            "goal_id" : self.goal_value
    
        }))

    def to_dict(self):
        return (dict(task={
            "id" : self.task_id,
            "title": self.title,
            "description" : self.description,
            "is_complete" : bool(self.completed_at)
        }))