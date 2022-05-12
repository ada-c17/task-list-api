from inspect import getargvalues
from operator import getitem
from app import db
from datetime import datetime
from dateutil import parser
from app.models.common import MissingValueError, FormatError

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship('Goal', back_populates='tasks')
    
    @staticmethod
    def interpret_timestamp(timestamp):
        if type(timestamp) != str:
            raise FormatError
        try:
            interpreted_time = parser.parse(timestr=timestamp)
        except:
            raise FormatError
        return interpreted_time

    @classmethod
    def new_task(cls, task_details):
        # Validate and process input before creation
        if 'title' not in task_details or 'description' not in task_details:
            raise MissingValueError
        if 'completed_at' not in task_details:
            task_details['completed_at'] = None
        elif ((time := task_details.get('completed_at'))
                and not isinstance(time, datetime)):
            task_details['completed_at'] = Task.interpret_timestamp(time)
        
        return cls(
            title = task_details['title'],
            description = task_details['description'],
            completed_at = task_details['completed_at']
        )
    
    def update(self, new_details):
        if ((time := new_details.get('completed_at'))
                and not isinstance(time, datetime)):
            new_details['completed_at'] = Task.interpret_timestamp(time)
        
        for k,v in new_details.items():
            if k in self.__dict__:
                setattr(self, k, v)
    
