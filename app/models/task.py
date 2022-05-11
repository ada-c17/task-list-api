from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        return dict(
        id=self.task_id,
        title=self.title,
        description=self.description,
        is_complete= bool(self.completed_at)
    )

    def to_dict_with_goal(self):
        return dict(
        id=self.task_id,
        goal_id=self.goal_id,
        title=self.title,
        description=self.description,
        is_complete= bool(self.completed_at)
    )