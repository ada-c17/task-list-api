from app import db

'''
task_id: a primary key for each task
title: text to name the task
description: text to describe the task
completed_at: a datetime that has the date that a 
task is completed on. Can be nullable, and contain a 
null value. A task with a null value for completed_at has 
not been completed. When we create a new task, completed_at 
should be null AKA None in Python.'''


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    is_complete = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, default=None)


    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=self.is_complete 

        )

    def to_dict_one_task(self):
        return {
            "task": {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.is_complete
            }
        }
  
 
        

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            title=data_dict["title"],
            description=data_dict["description"],
            # is_complete=data_dict["is_complete"],
            
        )

    #  def replace_details(self, data_dict):
    #     self.name=data_dict["name"]
    #     self.description=data_dict["description"]
    #     self.life=data_dict["life"]
    #     self.moons=data_dict["moons"]
    #     return self.to_dict()



    # completed_at : default null (none)

    # is_complete(db.relationship)


    # when we care a new task, completed_att should be NULL (NONE)







