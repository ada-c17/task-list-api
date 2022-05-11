from app import db

class Task(db.Model):
    ## class variables
    expected_elements = {"title":str, "description":str}
    db_name = "Task"

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id")) #note: need to make nullable? or that way by default?
    goal = db.relationship("Goal", back_populates="tasks") #lazy=select/True is default

    def make_response_dict(self):
        if self.completed_at:
            completed = True
        else:
            completed = False
        task_dict = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": completed
        }
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id
        return task_dict 