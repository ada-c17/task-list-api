from urllib import response
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)
    
    def to_dict(self):
        task_list = []
        for task in self.tasks:
            task_list.append(task.to_dict())
        
        goal_dict =  {
            "id": self.goal_id,
            "title": self.title
            }
        
        if task_list:
            goal_dict["tasks"] = task_list
        return goal_dict

    
#Change ownership of .
#And in order to do that I would create a route inside of drivers, a nested route, where I would pass in as
# a post the list of all the ids of the cars that I was then going to attach to that driver.\q