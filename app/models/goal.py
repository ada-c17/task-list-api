from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal")

# class Goal(db.Model):
#     goal_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    #title = db.Column(db.String)
    #tasks = db.relationship("Task", back_populates="goal", lazy = True)

# adding in lazy = True but could not update model due to migrations issue.

