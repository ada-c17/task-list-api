from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    # task_id = db.Column(db.Integer, db.ForeignKey('task.task_id'))
    tasks = db.relationship("Task", back_populates="goal")