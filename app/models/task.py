from multiprocessing.sharedctypes import Value
from app import db

#child class
class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String) 
    """set to index=True, unique=True avoids duplication of values. 
       Due to this program originally designed to allow duplication, by switching it to to unique would change my database
       (even I can just delete the db and re-create it), I decided to leave it as it is"""
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable = True)
    goal = db.relationship("Goal", back_populates="tasks")
        
    def to_json(self):
        task_dict = {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
        }
        
        

        if self.completed_at:
            task_dict["is_complete"] = True
        else:
            task_dict["is_complete"] = False
        
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id
       
        return task_dict