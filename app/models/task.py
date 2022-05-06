from app import db


class Task(db.Model):
    expected_elements = {"title":str, "description":str}

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None)

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
        return task_dict #if i put functions in the class, do I 
        #have to do a db migration?