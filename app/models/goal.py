from app import db



class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title=db.Column(db.String)
    tasks=db.relationship("Task",back_populates="goal",lazy = True) # lazy=true: get all the tasks objects when I query the database
    # will load the data as necessary in one go using a standard select statement
