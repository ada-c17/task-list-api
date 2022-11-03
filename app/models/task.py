from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    completed_at = db.Column(db.DateTime, nullable= True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates = "tasks")
