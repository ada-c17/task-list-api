from app import db

#parent class
class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)
    
    def to_json(self):
        return {
            "id" : self.goal_id,
            "title" : self.title,
       
        }
        
    
    def to_json2(self):
        goal_dict = {
            "id" : self.goal_id,
            "title" : self.title,
            "tasks": []
        }
        
        if self.tasks:
            for task in self.tasks:
        #         goal_dict["tasks"] = [{
        #         "id": task.task_id,
        #         "goal_id": task.goal_id,
        #         "title": task.title,
        #         "description": task.description,
        #         "is_complete": task.completed_at
        # }]
                goal_dict["tasks"] = [task.to_json()]
             
        return goal_dict
        
    