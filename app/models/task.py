from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)

    def create_task_dict(self):
        task_dict = {
                "id": self.task_id,
                "title": self.title,
                "description": self.description
        }
        if self.completed_at is None:
            task_dict["is_complete"] = False
        else:
            task_dict["is_complete"] = True

        if self.goal_id:
            task_dict["goal_id"] = self.goal_id
        
        return task_dict
        