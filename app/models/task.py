from __future__ import annotations
from app import db
from datetime import datetime
from dateutil import parser
from flask import abort
from app.error_responses import MissingValueError, FormatError, make_error_response

class Task(db.Model):
    '''A SQLAlchemy.Model subclass representing task entries in the database.
    
    Tasks can optionally be associated with a Goal instance which collects
    related sets of tasks.

    Attributes:
        task_id: int
        title: str
        description: str
        completed_at: datetime | None
        goal_id: int | None
        goal: Goal | None
    '''

    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship('Goal', back_populates='tasks')
    
    @staticmethod
    def interpret_timestamp(timestamp: str) -> datetime:
        '''Converts string input to datetime object using dateutil parser.'''

        try:
            interpreted_time = parser.parse(timestr=timestamp)
        except:
            abort(make_error_response(FormatError()))
        return interpreted_time

    @classmethod
    def create(cls, task_details: dict) -> Task:
        '''Creates and returns a new Task instance from input dict.'''

        # Validate and process input before creation
        if 'title' not in task_details or 'description' not in task_details:
            abort(make_error_response(MissingValueError(), cls))
        if 'completed_at' not in task_details:
            task_details['completed_at'] = None
        elif ((time := task_details.get('completed_at')) # Value is not None
                and not isinstance(time, datetime)):     # and not a datetime
            task_details['completed_at'] = Task.interpret_timestamp(str(time))
        
        return cls(
            title = task_details['title'],
            description = task_details['description'],
            completed_at = task_details['completed_at']
        )
    
    def update(self, new_details: dict) -> None:
        '''Updates the attributes of an existing Task instance.'''

        if ((time := new_details.get('completed_at')) # Value is not None
                and not isinstance(time, datetime)):  # and not a datetime
            new_details['completed_at'] = Task.interpret_timestamp(time)
        
        for k,v in new_details.items():
            if k in self.__dict__:
                setattr(self, k, v)
