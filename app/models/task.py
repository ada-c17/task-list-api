from app import db

#child class
class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String) #index=True, unique=True with or without don't work for unique value
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable = True)
    goal = db.relationship("Goal", back_populates="tasks")
    
    #depends on None(code)/null(db)
    # def completed(self):
    #     if not self.completed_at:
    #         return False
    #     else:
    #         return True
    
    #display jsonify dict
    
        
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