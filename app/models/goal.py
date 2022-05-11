from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship('Task', back_populates='goal')

    def to_json(self, include_tasks=False):
        if not include_tasks:
            return {
                'id': self.goal_id,
                'title': self.title
            }
        return {
            'id': self.goal_id,
            'title': self.title,
            'tasks': [task.to_json() for task in self.tasks]
        }