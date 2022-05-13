from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship



class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable= True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable = True)
    goal = db.relationship("Goal", back_populates="tasks")

    #completed_at is default = None)
    #instance method
    def to_json(self):
        # if self.goal_id:
        #     return dict(
        #         id=self.task_id,
        #         title=self.title,
        #         description=self.description,
        #         goal_id = self.goal_id,
        #         # is_complete=self.completed_at is not None
        #         is_complete = True if self.completed_at else False
        #     )
        # else:
            # return dict(
            #     id=self.task_id,
            #     title=self.title,
            #     description=self.description,
            #     # is_complete=self.completed_at is not None
            #     is_complete = True if self.completed_at else False
            # )

        task = dict(
            id=self.task_id,
            title=self.title,
            description=self.description,
            # is_complete=self.completed_at is not None
            is_complete = True if self.completed_at else False
        )
        if self.goal_id:
            task["goal_id"]=self.goal_id
        return task
        

    #helper function class method
    # @classmethod
    # def from_dict(cls, data_dict):
    #     return cls(
    #         title=data_dict["title"],
    #         description=data_dict["description"],
    #         # completed_at=data_dict["completed_at"], #what should this be?
    #         )