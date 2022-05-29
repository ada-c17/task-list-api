from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable =True)
    id=db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable =True)
    goal = db.relationship("Goal", back_populates="tasks")


    def to_dict(self):
        dict= { 
            "task": {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at)
            }}
        if self.id:
            dict["task"]["goal_id"]=self.id    
        return dict    

