from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="tasks")

    def task_dictionary(self):
        basic_dictionary = {
            "id":self.task_id,
            "title":self.title,
            "description":self.description
        }
        if self.completed_at is None:
            basic_dictionary["is_complete"] = False
        else:
            basic_dictionary["is_complete"] = True
        
        if self.goal_id is not None:
            basic_dictionary["goal_id"] = self.goal_id
        
        return {
            "task": basic_dictionary
        }
