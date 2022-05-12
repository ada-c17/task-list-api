from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None)
    is_complete = db.Column(db.Boolean, default=False)
    # goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    # goal = db.relationship("Goal", back_populates="tasks")
    
    def get_dict(self):
        rsp_json = {
            "id" : self.task_id,
            "title" : self.title,
            "description" : self.description,
            "is_complete" : self.completed_at is not None
        }
        # if self.goal_id:
            # rsp_json['goal_id'] = self.goal_id
            
        return rsp_json


    
# class Task(db.Model):
#     task_id = db.Column(db.Integer, primary_key=True)
#     task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     title = db.Column(db.String, nullable=False)
#     description = db.Column(db.String, nullable=False)
#     completed_at = db.Column(db.DateTime, nullable=True)