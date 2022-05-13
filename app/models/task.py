from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default = None)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))
    goal = db.relationship("Goal", back_populates="tasks")

# class Task(db.Model):
#     task_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
#     title = db.Column(db.String)
#     description = db.Column(db.String)
#     completed_at = db.Column(db.DateTime, default = None)
#     goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
#     goal = db.relationship("Goal", back_populates="tasks")

#adding in nullable = True as comment but could not update model due to migrations issue. 